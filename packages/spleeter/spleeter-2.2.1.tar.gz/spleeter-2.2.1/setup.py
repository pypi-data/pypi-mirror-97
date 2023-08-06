# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spleeter',
 'spleeter.audio',
 'spleeter.model',
 'spleeter.model.functions',
 'spleeter.model.provider',
 'spleeter.resources',
 'spleeter.utils']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python==0.2.0',
 'httpx[http2]>=0.16.1,<0.17.0',
 'librosa==0.8.0',
 'norbert==0.2.1',
 'numpy>=1.16.0,<1.19.0',
 'pandas==1.1.2',
 'tensorflow==2.3.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.7"': ['importlib-resources>=4.1.1,<5.0.0'],
 ':python_version < "3.8"': ['importlib-metadata>=3.0.0,<4.0.0'],
 'evaluation': ['musdb==0.3.1', 'museval==0.3.0']}

entry_points = \
{'console_scripts': ['spleeter = spleeter.__main__:entrypoint']}

setup_kwargs = {
    'name': 'spleeter',
    'version': '2.2.1',
    'description': 'The Deezer source separation library with pretrained models based on tensorflow.',
    'long_description': '<img src="https://github.com/deezer/spleeter/raw/master/images/spleeter_logo.png" height="80" />\n\n[![Github actions](https://github.com/deezer/spleeter/workflows/pytest/badge.svg)](https://github.com/deezer/spleeter/actions) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spleeter) [![PyPI version](https://badge.fury.io/py/spleeter.svg)](https://badge.fury.io/py/spleeter) [![Conda](https://img.shields.io/conda/vn/deezer-research/spleeter)](https://anaconda.org/deezer-research/spleeter) [![Docker Pulls](https://img.shields.io/docker/pulls/deezer/spleeter)](https://hub.docker.com/deezer/spleeter) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deezer/spleeter/blob/master/spleeter.ipynb) [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/spleeter/community) [![status](https://joss.theoj.org/papers/259e5efe669945a343bad6eccb89018b/status.svg)](https://joss.theoj.org/papers/259e5efe669945a343bad6eccb89018b)\n\n> :warning: [Spleeter 2.1.0](https://pypi.org/project/spleeter/) release introduces some breaking changes, including new CLI option naming for input, and the drop\n> of dedicated GPU package. Please read [CHANGELOG](CHANGELOG.md) for more details.\n\n## About\n\n**Spleeter** is [Deezer](https://www.deezer.com/) source separation library with pretrained models\nwritten in [Python](https://www.python.org/) and uses [Tensorflow](https://tensorflow.org/). It makes it easy\nto train source separation model (assuming you have a dataset of isolated sources), and provides\nalready trained state of the art model for performing various flavour of separation :\n\n* Vocals (singing voice) / accompaniment separation ([2 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-2stems-model))\n* Vocals / drums / bass / other separation ([4 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-4stems-model))\n* Vocals / drums / bass / piano / other separation ([5 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-5stems-model))\n\n2 stems and 4 stems models have [high performances](https://github.com/deezer/spleeter/wiki/Separation-Performances) on the [musdb](https://sigsep.github.io/datasets/musdb.html) dataset. **Spleeter** is also very fast as it can perform separation of audio files to 4 stems 100x faster than real-time when run on a GPU.\n\nWe designed **Spleeter** so you can use it straight from [command line](https://github.com/deezer/spleeter/wiki/2.-Getting-started#usage)\nas well as directly in your own development pipeline as a [Python library](https://github.com/deezer/spleeter/wiki/4.-API-Reference#separator). It can be installed with [Conda](https://github.com/deezer/spleeter/wiki/1.-Installation#using-conda),\nwith [pip](https://github.com/deezer/spleeter/wiki/1.-Installation#using-pip) or be used with\n[Docker](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-docker-image).\n\n### Projects and Softwares using **Spleeter**\n\nSince it\'s been released, there are multiple forks exposing **Spleeter** through either a Guided User Interface (GUI) or a standalone free or paying website. Please note that we do not host, maintain or directly support any of these initiatives.\n\nThat being said, many cool projects have been built on top of ours. Notably the porting to the *Ableton Live* ecosystem through the [Spleeter 4 Max](https://github.com/diracdeltas/spleeter4max#spleeter-for-max) project.\n\n**Spleeter** pre-trained models have also been used by professionnal audio softwares. Here\'s a non-exhaustive list:\n\n* [iZotope](https://www.izotope.com/en/shop/rx-8-standard.html) in its *Music Rebalance* feature within **RX 8**\n* [SpectralLayers](https://new.steinberg.net/spectralayers/) in its *Unmix* feature in **SpectralLayers 7**\n* [Acon Digital](https://acondigital.com/products/acoustica-audio-editor/) within **Acoustica 7**\n* [VirtualDJ](https://www.virtualdj.com/stems/) in their stem isolation feature\n* [Algoriddim](https://www.algoriddim.com/apps) in their **NeuralMix** and **djayPRO** app suite\n\n## Quick start\n\nWant to try it out but don\'t want to install anything ? We have set up a [Google Colab](https://colab.research.google.com/github/deezer/spleeter/blob/master/spleeter.ipynb).\n\nReady to dig into it ? In a few lines you can install **Spleeter** using [Conda](https://github.com/deezer/spleeter/wiki/1.-Installation#using-conda) and separate the vocal and accompaniment parts from an example audio file:\n\n```bash\n# install using conda\nconda config --add channels conda-forge # only needed if you don\'t already have this channel set\nconda install -c deezer-research spleeter \n# download an example audio file (if you don\'t have wget, use another tool for downloading)\nwget https://github.com/deezer/spleeter/raw/master/audio_example.mp3\n# separate the example audio into two components\nspleeter separate -p spleeter:2stems -o output audio_example.mp3\n```\n> :warning: for Mac Users, this will work but will install an old version of spleeter. To get the latest version, you need to install **Spleeter** using `pip`. Check the [wiki](https://github.com/deezer/spleeter/wiki/1.-Installation) for details.\n\nYou should get two separated audio files (`vocals.wav` and `accompaniment.wav`) in the `output/audio_example` folder.\n\nFor a detailed documentation, please check the [repository wiki](https://github.com/deezer/spleeter/wiki/1.-Installation)\n\n## Development and Testing\n\nThis project is managed using [Poetry](https://python-poetry.org/docs/basic-usage/), to run test suite you\ncan execute the following set of commands:\n\n```bash\n# Clone spleeter repository\ngit clone https://github.com/Deezer/spleeter && cd spleeter\n# Install poetry\npip install poetry\n# Install spleeter dependencies\npoetry install\n# Run unit test suite\npoetry run pytest tests/\n```\n\n## Reference\n\n* Deezer Research - Source Separation Engine Story - deezer.io blog post:\n  * [English version](https://deezer.io/releasing-spleeter-deezer-r-d-source-separation-engine-2b88985e797e)\n  * [Japanese version](http://dzr.fm/splitterjp)\n* [Music Source Separation tool with pre-trained models / ISMIR2019 extended abstract](http://archives.ismir.net/ismir2019/latebreaking/000036.pdf)\n\nIf you use **Spleeter** in your work, please cite:\n\n```BibTeX\n@article{spleeter2020,\n  doi = {10.21105/joss.02154},\n  url = {https://doi.org/10.21105/joss.02154},\n  year = {2020},\n  publisher = {The Open Journal},\n  volume = {5},\n  number = {50},\n  pages = {2154},\n  author = {Romain Hennequin and Anis Khlif and Felix Voituret and Manuel Moussallam},\n  title = {Spleeter: a fast and efficient music source separation tool with pre-trained models},\n  journal = {Journal of Open Source Software},\n  note = {Deezer Research}\n}\n```\n\n## License\n\nThe code of **Spleeter** is [MIT-licensed](LICENSE).\n\n## Disclaimer\n\nIf you plan to use **Spleeter** on copyrighted material, make sure you get proper authorization from right owners beforehand.\n\n## Troubleshooting\n\n**Spleeter** is a complex piece of software and although we continously try to improve and test it you may encounter unexpected issues running it. If that\'s the case please check the [FAQ page](https://github.com/deezer/spleeter/wiki/5.-FAQ) first as well as the list of [currently open issues](https://github.com/deezer/spleeter/issues)\n\n### Windows users\n\n   It appears that sometimes the shortcut command `spleeter` does not work properly on windows. This is a known issue that we will hopefully fix soon. In the meantime replace `spleeter separate` by `python -m spleeter separate` in command line and it should work.\n\n## Contributing\n\nIf you would like to participate in the development of **Spleeter** you are more than welcome to do so. Don\'t hesitate to throw us a pull request and we\'ll do our best to examine it quickly. Please check out our [guidelines](.github/CONTRIBUTING.md) first.\n\n## Note\n\nThis repository include a demo audio file `audio_example.mp3` which is an excerpt\nfrom Slow Motion Dream by Steven M Bryant (c) copyright 2011 Licensed under a Creative\nCommons Attribution (3.0) [license](http://dig.ccmixter.org/files/stevieb357/34740)\nFt: CSoul,Alex Beroza & Robert Siekawitch\n',
    'author': 'Deezer Research',
    'author_email': 'spleeter@deezer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deezer/spleeter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.9',
}


setup(**setup_kwargs)
