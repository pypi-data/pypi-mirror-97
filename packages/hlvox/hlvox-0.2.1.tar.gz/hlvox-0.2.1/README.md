# HLVox

[![pipeline status](https://gitlab.com/bhagen/hlvox/badges/master/pipeline.svg)](https://gitlab.com/bhagen/hlvox/commits/master)
[![coverage report](https://gitlab.com/bhagen/hlvox/badges/master/coverage.svg)](https://gitlab.com/bhagen/hlvox/commits/master)
[![PyPI version](https://badge.fury.io/py/hlvox.svg)](https://badge.fury.io/py/hlvox)

Originally intended to create sentences from the word snippets for the 
Half Life 1 Vox, this project can take a folder of word audio files and piece 
them into sentences that are exported as audio files.

## Getting Started

To use this project, you will first need a folder full of voice files.
If you have Half Life 1 installed, the voices can be extracted from the VPK 
files using something like GCFScape.

### Prerequisites

HLVox is written using Python 3.7.2, developed in VSCode with autopep8 
and flake8.

HLVox requires the following Python packages to operate:

```
PyDub
TinyDB
```

As well as an installation of FFMpeg. On Ubuntu, just run the following:

```
apt update
apt install ffmpeg
```

### Installing

How to set up a basic dev environment:

Pull this repo

```
git pull https://gitlab.com/bhagen/hlvox.git
```

Change into the new repo directory

```
cd hlvox
```

Install requirements
```
pip install -r requirements.py
```

### Quick Start

If you want to jump right into generating a sentence, grab a folder full
of voice files, maybe call it `hl1` and put it in the repo you pulled before. 
Also make a folder called `exports` in the base folder.

Enter Python shell
```
python
```

Import the voice submodule
```
from hlvox import Voice
```

Make a voice object using your voice and exports folder
```
v = Voice('./hl1', './exports')
```

Generate your first sentence!
```
v.generate_audio("hello")
```

Your sentence should be called `1.wav` (or some other audio format) and be
waiting for you in the `exports` folder.


## Running the tests

```
pytest
```

## Documentation Generation

I used [Sphinx](http://www.sphinx-doc.org) to create autodoc documentation
from docstrings in the modules.

Change into doc directory
```
cd doc
```

(If you've modified the source code, grab the new apidocs
```
sphinx-apidoc -f -o ./source ../hlvox
```


Generate documentation
```
make html
```


## Authors

* **Blair Hagen** - *Initial work* - [bhagen](https://github.com/bhagen)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Valve for making such an amazing voice
