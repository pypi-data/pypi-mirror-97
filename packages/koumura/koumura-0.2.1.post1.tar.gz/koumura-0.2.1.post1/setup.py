# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['koumura']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1']

setup_kwargs = {
    'name': 'koumura',
    'version': '0.2.1.post1',
    'description': 'Functions for working with this data repository: https://figshare.com/articles/BirdsongRecognition/3470165',
    'long_description': '![Build Status](https://github.com/NickleDave/koumura/actions/workflows/ci.yml/badge.svg)\n![DOI](https://zenodo.org/badge/159952839.svg)\n![PyPI version](https://badge.fury.io/py/koumura.svg)\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n# koumura\nFunctions for working with data from the following repository:\n<https://figshare.com/articles/BirdsongRecognition/3470165>  \n\nThe repository contains .wav files of Bengalese finch song from ten birds\nand annotation for the songs in .xml files.\n\nThis repository provides a great resource, and was used to benchmark\na sliding window-based neural network for segmenting and labeling\nthe elements of birdsong, as described in the following paper:  \nKoumura, Takuya, and Kazuo Okanoya.  \n"Automatic recognition of element classes and boundaries in the birdsong\nwith variable sequences."  \nPloS one 11.7 (2016): e0159188.  \n<https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0159188>  \n\nThe code for the network can be found here:  \n<https://github.com/takuya-koumura/birdsong-recognition>\n\nThe original code was released under the GNU license:  \n<https://github.com/takuya-koumura/birdsong-recognition/blob/master/LICENSE>\n\nThe `koumura` module is used with the [`crowsetta`](https://github.com/NickleDave/crowsetta)\n package to make the repository a dataset available in the\n[`hybrid-vocal-classifier`](https://hybrid-vocal-classifier.readthedocs.io/en/latest/)\nand [`vak`](https://github.com/NickleDave/vak) libraries.\n\nIt\'s called `koumura` because that\'s the last name of the first author\non the paper, and because I am too lazy to type `PyBirdsongRecognition`.\n\n### Installation\n`$ pip install koumura`\n\n### Usage\n\nThe main thing that `koumura` gives you is easy access to the\nannotation, without having to deal with the .xml file format.\n\nTo access the annotation in the `Annotation.xml` files for each bird,\nuse the `parse_xml` function.\n```Python\n>>> from koumura import parse_xml\n>>> seq_list = parse_xml(xml_file=\'./Bird0/Annotation.xml\', concat_seqs_into_songs=False)\n>>> seq_list[0]\nSequence from 0.wav with position 32000 and length 43168\n>>> seq_list[0].syls[:3]\n[Syllable labeled 0 at position 2240 with length 2688, Syllable labeled 0 at position 8256 with length 2784, Syllable labeled 0 at position 14944 with length 2816]  \n```\n\nNotice that this package preserves the abstraction of the original code,\nwhere syllables and sequences of syllables are represented as objects.\nThis can be helpful if you are trying to replicate functionality from\nthat code.  \n**Importantly, each song is broken up into a number of "sequences".**\nYou can set the flag `concat_seqs_into_songs` to `True` if you want\n`parse_xml` to concatenate sequences by song (.wav file), so that each\nSequence is actually all the sequences from one song.  \nIf you are using the annotation to work with the dataset for\nsome other purpose, you may find it more convenient to work with some\nother format. For that, please check out the\n[`crowsetta`](https://github.com/NickleDave/crowsetta)\ntool, that helps with building datasets of annotated vocalizations\nin a way that\'s annotation-format agnostic.\n\nThe `koumura` package also provides a convenience function to load the annotation\nfor an individual song, `load_song_annot`. This is basically a wrapper\naround `parse_xml` that filters out the songs you don\'t want.\n```Python\n>>> from koumura import load_song_annot\n>>> wav1 = load_song_annot(wav_file=\'1.wav\')\n>>> print(wav1)                                                                                                  \nSequence from 1.wav with position 32000 and length 214176  \n```\n\n### Getting Help\nPlease feel free to raise an issue here:  \nhttps://github.com/NickleDave/koumura/issues\n\n### License\n[BSD License](./LICENSE).\n\n### Citation\nIf you use this package, please cite the DOI:\n[![DOI](https://zenodo.org/badge/159952839.svg)](https://zenodo.org/badge/latestdoi/159952839)\n',
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickleDave/koumura',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
