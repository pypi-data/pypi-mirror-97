import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Union

from pydub import AudioSegment
from tinydb import TinyDB, where

log = logging.getLogger(__name__)


class Voice:
    def __init__(self, path: Union[Path, str], export_path: Union[Path, str], db_path: Union[Path, str]):
        self.path = Path(path)
        self.export_path = Path(export_path)

        self.info_path = self.path.joinpath("info/")
        self.info_name = "info.json"

        self.db_path = Path(db_path)
        self.db_name = "db.json"

        self.name = self.path.name

        self._punctuation = [",", "."]
        self._punctuation_timing = {",": 250, ".": 500}

        self.alarms: List[str] = []

        self._db = self._setup_db(self.db_path, self.db_name)

        self._word_dict = self._build_word_dict(self.path)
        self._audio_format = self._find_audio_format(
            self._word_dict)  # TODO: Use properies?

        self._read_info(self.info_path, self.info_name)

        # TODO: Should probably go somewhere else
        self.export_path.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._db.close()

    # TODO: Need a better way to handle this
    def exit(self):
        self._db.close()

    def _setup_db(self, path, db_name):
        path.mkdir(parents=True, exist_ok=True)
        return TinyDB(path.joinpath(db_name))

    def _build_word_dict(self, path) -> dict:
        word_dict = {}
        word_files = list(x for x in path.iterdir() if x.is_file())

        for word in word_files:
            word = Path(word)
            name = word.stem
            word_dict[name] = word

        self._validate_dictionary(word_dict)

        return word_dict

    def _read_info(self, path, info_name):
        info_path = path.joinpath(info_name)
        if info_path.exists():
            with open(info_path, 'r') as info_file:
                info = json.load(info_file)
                self.alarms = info["alarms"]
        log.info(f"Available alarms are {self.alarms}")

    def _validate_dictionary(self, word_dict):
        if len(word_dict) == 0:
            log.error("No words found")
            raise Exception("No words found")

    def _find_audio_format(self, word_dict) -> str:
        file_format = None
        for path in word_dict.values():
            if file_format == None:
                file_format = path.suffix[1:]
            else:
                if str(file_format) != str(path.suffix[1:]):
                    log.error(
                        "Inconsistent audio formats in the word dict")
                    raise Exception("Inconsistent Audio Formats")
        if not file_format:
            raise Exception("No file format found")
        log.info(f"Audio format found: {file_format}")
        return file_format

    def _process_sentence(self, sentence) -> list:
        """
        Takes a normally formatted sentence and breaks it into base elements

        Args:
            sentence (string): normally formatted sentence to be processed

        Returns:
            (array): array of elements in sentence
        """
        sentence = sentence.lower()
        sentence = sentence.rstrip()
        log.info(f"Processing sentence '{sentence}'")

        # Initial split on spaces
        split_sent = sentence.split(" ")

        # Pull out punctuation
        reduced_sent = []
        for item in split_sent:
            # find first punctuation mark, if any
            first_punct = next(
                (punct for punct in self._punctuation if punct in item), False)

            if first_punct:
                # Get its index
                first_punct_ind = item.find(first_punct)

                # Add everything before punct (the word)
                reduced_sent.append(item[:first_punct_ind])

                # Add all the punctuation if its actually punctuation
                # TODO: Figure out if I want to deal with types like ".hello" throwing out all the characters after the period.
                for punct in item[first_punct_ind:]:
                    if punct in self._punctuation:
                        reduced_sent.append(punct)

            else:
                reduced_sent.append(item)

        # Clean blanks from reduced_sent
        if '' in reduced_sent:
            reduced_sent = [value for value in reduced_sent if value != '']

        log.info(f"Sentence processed: '{reduced_sent}'")
        return reduced_sent

    def _get_sayable_words(self, processed_sentence_arr, word_dict) -> list:
        sayable = [
            word for word in processed_sentence_arr if word in word_dict or word in self._punctuation]
        sayable_dedup = list(dict.fromkeys(sayable))  # removes duplicates
        sayable_dedup.sort()
        return sayable_dedup

    def _get_unsayable_words(self, processed_sentence_arr, sayable_words) -> list:
        unsayable = list(set(processed_sentence_arr) - set(sayable_words))
        return list(dict.fromkeys(unsayable))  # removes duplicates

    def _get_sayable_sentence_arr(self, processed_sentence_arr, sayable_words) -> list:
        return [word for word in processed_sentence_arr if word in sayable_words]

    def _create_sentence_string(self, words) -> str:
        if len(words) == 1:
            return words[0]
        else:
            return " ".join(words)

    def get_words(self) -> list:
        """Gets the available words for the voice
        Returns:
            (list): Words available to the voice
        """
        word_list = list(self._word_dict.keys())
        word_list.sort()
        return word_list

    def get_audio_format(self) -> str:
        """Get the audio format of the voice files as well as generated files
        Returns:
            (string): Audio format
        """
        return self._audio_format

    def get_filepath_from_sent(self, sentence):
        """
        Gets the filepath of an already generated sentence

        Args:
            sentence (string): The sentence to search for. Should be normally formatted already.
        Returns:
            (pathlib): Path to the desired sentence, or None if not found.
        """
        sentence = self.get_sentence_string(sentence)
        q = self._db.search(where("sentence") == sentence)

        if len(q) == 0:
            return None
        elif len(q) == 1:
            return Path(self.export_path, str(q[0].doc_id) + "." + self._audio_format)
        else:
            log.error("Multiple entries for same sentence in DB")
            raise Exception("DB Error")

    def get_sayable(self, sentence) -> list:
        """Gets the words that the voice can say from a sentence

        Args:
            sentence (string): Sentence to check for sayable words
        Returns:
            (list): Words that can be said
        """

        proc_sentence = self._process_sentence(sentence)
        return self._get_sayable_words(proc_sentence, self._word_dict)

    def get_unsayable(self, sentence) -> list:
        """Gets the words that the voice cannot say from a sentence

        Args:
            sentence (string): Sentence to check for un-sayable words
        Returns:
            (list): Words that cannot be said
        """

        proc_sentence = self._process_sentence(sentence)
        sayable_words = self._get_sayable_words(proc_sentence, self._word_dict)
        return self._get_unsayable_words(proc_sentence, sayable_words)

    def get_sentence_list(self, sentence) -> list:
        """Converts sentence into list of words that can be said

        Args:
            sentence (string): Sentence to convert to list
        Returns:
            (list): Sentence in list format excluding words that cannot be said
        """

        proc_sentence = self._process_sentence(sentence)
        sayable_words = self._get_sayable_words(proc_sentence, self._word_dict)
        return self._get_sayable_sentence_arr(proc_sentence, sayable_words)

    def get_sentence_string(self, sentence):
        proc_sentence = self._process_sentence(sentence)
        sayable_words = self._get_sayable_words(
            proc_sentence, self._word_dict)
        sayable_sent_arr = self._get_sayable_sentence_arr(
            proc_sentence, sayable_words)

        return self._create_sentence_string(sayable_sent_arr)

    def get_generated_sentences(self) -> list:
        """Gets the previously generated sentence strings

        Returns:
            (list): List of sentence strings generated previously
        """
        return [entry["sentence"] for entry in self._db.all()]

    def generate_audio(self, sentence, force_remake=False) -> dict:
        """Generates an audio file from the given sentence

        Args:
            sentence (string): Sentence string to be generated
            start_pad (int): Silence in ms to pad beginning of file with
        Returns:
            (dict): Information about generated sentence with the following format:
            {"sentence": (string) The converted, normally formatted sentence string that was generated,
             "sayable": (list) The words in the sentence that are sayable,
             "unsayable": (list) The words in the sentence that are unsayable,
             "path": (pathlib) The path to the generated file, or None if no sentence can be created}
        """

        log.info(f"Asked to generate {sentence}")
        proc_sentence = self._process_sentence(sentence)

        sayable_words = self._get_sayable_words(proc_sentence, self._word_dict)
        sayable_sent_arr = self._get_sayable_sentence_arr(
            proc_sentence, sayable_words)
        sayable_sent_str = self._create_sentence_string(sayable_sent_arr)
        unsayable_worlds = self._get_unsayable_words(
            proc_sentence, sayable_words)

        return_dict = {
            "sentence": sayable_sent_str,
            "sayable": sayable_words,
            "unsayable": unsayable_worlds,
            "path": None
        }

        log.debug(f"Generating {sayable_sent_str}")

        words_audio = []

        # Only create sentence if there are words to put in it
        if len(sayable_words) == 0:
            log.warning(
                f"Can't say any words in {sentence}, not generating")
            return return_dict

        # Search in DB for sentence string
        q = self._db.search(where("sentence") == sayable_sent_str)
        # if it doesn't exist, add it and get the ID to use as filename, then create file and save
        # if it does exist, return the ID as a path to the file
        log.debug(f"Looking for {sayable_sent_str} Found: {q}")

        # If sentence already exists, don't recreate, just return the existing path
        if len(q) >= 1 and not force_remake:
            if len(q) > 1:
                log.error(
                    f"Database error. Num of queries for sentence is {len(q)}. Using first result")
            log.info(
                f"Sentence {sayable_sent_str} already exists, not recreating")
            save_path = Path(self.export_path,
                             str(q[0].doc_id) + "." + self._audio_format)
            return_dict["path"] = save_path
            return return_dict

        # If sentence doesn't exist, create it (or overwrite if we are forcing remakes)
        sent_id = self._db.insert({"sentence": sayable_sent_str})

        for word in sayable_sent_arr:
            if word in self._punctuation_timing:
                words_audio.append(AudioSegment.silent(
                    self._punctuation_timing[word]))
            else:
                words_audio.append(AudioSegment.from_file(
                    self._word_dict[word], self._audio_format))

        sentence_audio = words_audio.pop(0)
        for word_audio in words_audio:
            word_audio = word_audio.set_frame_rate(sentence_audio.frame_rate)
            sentence_audio = sentence_audio + word_audio

        save_path = Path(self.export_path, str(
            sent_id) + "." + self._audio_format)
        sentence_audio.export(save_path, format=self._audio_format)

        return_dict["path"] = save_path
        return return_dict

    def get_generated_sentences_dict(self) -> dict:
        """Gets the previously generated sentence strings
        along with their corresponding ID in the database

        Returns:
            (dict): Dict of sentence and id pairs
        """
        entries = self._db.all()
        return {entries.index(entry): entry["sentence"] for entry in entries}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Generate a sentence using a voice')
    parser.add_argument('-s', '--voice-dir', type=str, required=True)
    parser.add_argument('-e', '--export-dir', type=str, required=True)
    parser.add_argument('-d', '--db', type=str, required=True)
    parser.add_argument('sentence', type=str)
    parser.add_argument('-f', '--force', action='store_true', default=False)
    args = parser.parse_args()

    voice_dir = Path(args.voice_dir)
    if not voice_dir.is_dir():
        print(f'Voice dir at {voice_dir} does not exist!')
        sys.exit(1)

    export_dir = Path(args.export_dir)
    if not export_dir.is_dir():
        print(f'Export dir at {export_dir} does not exist!')
        sys.exit(1)

    db_path = Path(args.db)

    voice = Voice(path=voice_dir, export_path=export_dir, db_path=db_path)

    voice.generate_audio(args.sentence, force_remake=args.force)
