from pathlib import Path

import pytest
from hlvox import Voice

import utils as th

# Stand-in files for testing
normal_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
no_punct_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
inconst_format_files = ["hello.mp3", "my.wav", "name", "is.wav", "vox.mp4"]
no_format_files = ["imatextfile", "whatami"]
alarm_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav",
               "dadeda.wav", "woop.wav"]
alph_files = ["a.wav", "b.wav", "c.wav"]


# test_filepath = "./tests/tempfiles"
# test_filepath_p = Path(test_filepath)
# test_exportpath = "./tests/tempexport"
# test_exportpath_p = Path(test_exportpath)
# test_dbpath = "./tests/tempdb"
# test_dbpath_p = Path(test_dbpath)

# Example info file
ex_info_file = {"alarms": ["dadeda", "woop"]}


# @pytest.fixture(scope="function")
# def test_voice_files(temp_path):
#     th.create_test_files(temp_path, test_files)
#     return temp_path


class TestFileHandling():
    def test_empty_files(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, [])
        with pytest.raises(Exception) as e:
            Voice(voice_dir,
                  tmp_path.joinpath("export"), tmp_path.joinpath("db"))

        assert str(e.value) == "No words found"

    def test_inconsistent_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, inconst_format_files)
        with pytest.raises(Exception) as e:
            Voice(voice_dir,
                  tmp_path.joinpath("export"), tmp_path.joinpath("db"))

        assert str(e.value) == "Inconsistent Audio Formats"

    def test_no_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, no_format_files)
        with pytest.raises(Exception) as e:
            Voice(voice_dir,
                  tmp_path.joinpath("export"), tmp_path.joinpath("db"))

        assert str(e.value) == "No file format found"

    def test_audio_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        with Voice(voice_dir,
                   tmp_path.joinpath("export"), tmp_path.joinpath("db")) as unit:
            assert unit.get_audio_format() == "wav"


class TestDictContents():
    def test_basic_dict(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        with Voice(voice_dir,
                   tmp_path.joinpath("export"), tmp_path.joinpath("db")) as unit:

            expected_names = [name[:-4] for name in normal_files]
            expected_names.sort()

            tu_dict = unit.get_words()

            assert expected_names == tu_dict

        def test_alphab(self, tmp_path: Path):
            voice_dir = th.create_voice_files(tmp_path, alph_files)
            with Voice(voice_dir,
                       tmp_path.joinpath("export"), tmp_path.joinpath("db")) as unit:

                expected_names = ["a", "b", "c"]

                tu_dict = unit.get_words()

                assert expected_names == tu_dict

    class TestVoiceInfoLoading():
        def test_alarm_read(self, tmp_path: Path):
            voice_dir = th.create_voice_files(tmp_path, normal_files)
            th.create_info(ex_info_file, voice_dir)
            with Voice(voice_dir,
                       tmp_path.joinpath("export"), tmp_path.joinpath("db")) as unit:

                assert unit.alarms == ["dadeda", "woop"]


@pytest.fixture
def voice(tmp_path: Path):
    voice_dir = th.create_voice_files(tmp_path, normal_files)
    voice = Voice(voice_dir,
                  tmp_path.joinpath("export"), tmp_path.joinpath("db"))
    yield voice
    voice.exit()


class TestSentenceList():
    def test_empty_sentence(self, voice: Voice):
        ret = voice.get_sentence_list("")

        assert ret == []

    def test_simple_sentence(self, voice):
        ret = voice.get_sentence_list("hello")

        assert ret == ["hello"]

    def test_simple_punct(self, voice):
        ret = voice.get_sentence_list("hello, world")

        assert ret == ["hello", ","]

    def test_comp_punct(self, voice):
        ret = voice.get_sentence_list("hello , world. Vox , , says hi")

        assert ret == ["hello", ",", ".",
                       "vox", ",", ","]

    def test_punct_only(self, voice):
        ret = voice.get_sentence_list(",")

        assert ret == [","]

    def test_no_space_punct(self, voice):
        ret = voice.get_sentence_list(",.")

        assert ret == [",", "."]

    def test_temp(self, voice):
        ret = voice.get_sentence_list("hello. my name, is, vox")

        assert ret == ["hello", ".", "my", "name",
                       ",", "is", ",", "vox"]

    def test_punct_location(self, voice):
        # Not sure how to deal with types like ".hello"
        # for now it will treat it as just a period and throw out all the characters after it
        ret1 = voice.get_sentence_list("hello.")
        ret2 = voice.get_sentence_list(".hello")
        ret3 = voice.get_sentence_list(".hello.")

        assert ret1 == ["hello", "."]
        assert ret2 == ["."]
        assert ret3 == [".", "."]

    def test_trailing_whitespace(self, voice):
        ret1 = voice.get_sentence_list("hello ")
        ret2 = voice.get_sentence_list("hello\n")
        ret3 = voice.get_sentence_list("hello \n")
        ret4 = voice.get_sentence_list("hello \n\r")
        ret5 = voice.get_sentence_list("hello \n\r vox ")

        assert ret1 == ["hello"]
        assert ret2 == ["hello"]
        assert ret3 == ["hello"]
        assert ret4 == ["hello"]
        assert ret5 == ["hello", "vox"]


class TestFilenameFromSent():
    def test_not_gen_sent(self, voice: Voice):
        fp = voice.get_filepath_from_sent("hello")

        assert fp == None

    def test_simple_sent(self, voice: Voice):
        voice.generate_audio("hello")

        fp = voice.get_filepath_from_sent("hello")

        assert fp == voice.export_path.joinpath("1.wav")


class TestSayableUnsayable():
    def test_empty_sent(self, voice: Voice):
        ret_say = voice.get_sayable("")
        ret_unsay = voice.get_unsayable("")

        assert ret_say == []
        assert ret_unsay == []

    def test_simple_sent(self, voice: Voice):
        ret_say = voice.get_sayable("hello")
        ret_unsay = voice.get_unsayable("hello")

        assert ret_say == ["hello"]
        assert ret_unsay == []

    def test_duplicates(self, voice: Voice):
        sent = "hello hello world world , , . . duplicates! duplicates"

        ret_say = voice.get_sayable(sent)
        ret_unsay = voice.get_unsayable(sent)

        assert not set(ret_say) ^ set(["hello", ",", "."])
        assert not set(ret_unsay) ^ set(["world", "duplicates", "duplicates!"])

    def test_comp_sent(self, voice: Voice):
        sent = "hello, world. Vox can't say some of this."

        ret_say = voice.get_sayable(sent)
        ret_unsay = voice.get_unsayable(sent)

        assert not set(ret_say) ^ set(["hello", ",", "vox", "."])
        assert not set(ret_unsay) ^ set(
            ["world", "can't", "say", "some", "of", "this"]
        )

    def test_dup_punct(self, voice: Voice):
        sent = "hello... world"

        ret_say = voice.get_sayable(sent)
        ret_unsay = voice.get_unsayable(sent)

        assert not set(ret_say) ^ set(["hello", "."])
        assert not set(ret_unsay) ^ set(["world"])


@pytest.fixture
def exp_sentence_info():
    return {"sentence": None,
            "sayable": None,
            "unsayable": None,
            "path": None}


class test_sentence_generation():
    def test_empty_sent(self, voice: Voice, exp_sentence_info: dict):
        ret = voice.generate_audio("")
        exports = list(voice.export_path.iterdir())

        exp_sentence_info["sentence"] = ""
        exp_sentence_info["sayable"] = []
        exp_sentence_info["unsayable"] = []

        exp_exports = []

        assert ret == exp_sentence_info
        assert exp_exports == exports

    def test_unsayable_sent(self, voice: Voice, exp_sentence_info: dict):
        ret = voice.generate_audio("whatthefuckdidyoujustsaytome")
        exports = list(voice.export_path.iterdir())

        exp_sentence_info["sentence"] = ""
        exp_sentence_info["sayable"] = []
        exp_sentence_info["unsayable"] = ["whatthefuckdidyoujustsaytome"]

        exp_exports = []

        assert ret == exp_sentence_info
        assert exports == exp_exports

    def test_sayable_sent(self, voice: Voice, exp_sentence_info: dict):
        sentence = "hello, my name is vox"
        ret = voice.generate_audio(sentence)

        exp_path = voice.get_filepath_from_sent("hello , my name is vox")
        exports = list(voice.export_path.iterdir())

        exp_sentence_info["sentence"] = "hello , my name is vox"
        exp_sentence_info["sayable"] = [
            ",", "hello", "is", "my", "name", "vox"]
        exp_sentence_info["unsayable"] = []
        exp_sentence_info["path"] = exp_path

        exp_exports = [exp_path]

        assert ret == exp_sentence_info
        assert exports == exp_exports

    def test_duplicate_sent(self, voice: Voice, exp_sentence_info: dict):
        exp_path = voice.export_path.joinpath(
            "0.wav")
        voice.generate_audio("hello")
        voice.generate_audio("hello")

        exp_path = voice.get_filepath_from_sent("hello")

        exports = list(voice.export_path.iterdir())

        assert [exp_path] == exports

    def test_duplicate_words(self, voice: Voice, exp_sentence_info: dict):
        ret = voice.generate_audio("hello hello hello")
        exp_path = voice.get_filepath_from_sent("hello hello hello")
        exports = list(voice.export_path.iterdir())

        exp_sentence_info["sentence"] = "hello hello hello"
        exp_sentence_info["sayable"] = ["hello"]
        exp_sentence_info["unsayable"] = []
        exp_sentence_info["path"] = exp_path

        exp_exports = [exp_path]

        assert ret == exp_sentence_info
        assert exports == exp_exports

    def test_dup_punct(self, voice: Voice, exp_sentence_info: dict):
        ret = voice.generate_audio("hello... hello")
        exp_path = voice.get_filepath_from_sent("hello . . . hello")
        exports = list(voice.export_path.iterdir())

        exp_sentence_info["sentence"] = "hello . . . hello"
        exp_sentence_info["sayable"] = [".", "hello"]
        exp_sentence_info["unsayable"] = []
        exp_sentence_info["path"] = exp_path

        exp_exports = [exp_path]

        assert ret == exp_sentence_info
        assert exports == exp_exports

    def test_multiple_sent(self, voice: Voice):

        voice.generate_audio("hello")
        voice.generate_audio("vox")
        voice.generate_audio(".")
        voice.generate_audio(",")

        test_paths = []
        test_paths.append(voice.get_filepath_from_sent("hello"))
        test_paths.append(voice.get_filepath_from_sent("vox"))
        test_paths.append(voice.get_filepath_from_sent("."))
        test_paths.append(voice.get_filepath_from_sent(","))

        exp_paths = [voice.export_path.joinpath("1.wav"), voice.export_path.joinpath(
            "2.wav"), voice.export_path.joinpath("3.wav"), voice.export_path.joinpath("4.wav")]

        assert test_paths == exp_paths


class test_get_sayable_string():
    def test_simple_sent(self, voice: Voice):
        ret = voice.get_sentence_string("hello")

        assert ret == "hello"

    def test_comp_sent(self, voice: Voice):
        ret = voice.get_sentence_string("hello. my name, is, vox")

        assert ret == "hello . my name , is , vox"


class test_get_generated_sentences():
    def test_no_sentences(self, voice: Voice):
        ret = voice.get_generated_sentences()

        assert ret == []

    def test_single_sentences(self, voice: Voice):
        voice.generate_audio("hello")

        ret = voice.get_generated_sentences()

        assert ret == ["hello"]

    def test_multiple_sentences(self, voice: Voice):
        voice.generate_audio("hello")
        voice.generate_audio("vox")

        ret = voice.get_generated_sentences()

        assert ret == ["hello", "vox"]


class test_get_generated_sentences_dict():
    def test_no_sentences(self, voice: Voice):
        ret = voice.get_generated_sentences_dict()

        assert ret == {}

    def test_single_sentences(self, voice: Voice):
        voice.generate_audio("hello")

        ret = voice.get_generated_sentences_dict()

        assert ret == {0: "hello"}

    def test_multiple_sentences(self, voice: Voice):
        voice.generate_audio("hello")
        voice.generate_audio("vox")

        ret = voice.get_generated_sentences_dict()

        assert ret == {0: "hello", 1: "vox"}
