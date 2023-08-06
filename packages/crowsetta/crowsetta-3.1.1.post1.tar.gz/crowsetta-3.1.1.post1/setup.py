# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crowsetta', 'textgrid']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3',
 'attrs>=19.3.0',
 'evfuncs>=0.3.2',
 'koumura>=0.2.1',
 'numpy>=1.18.1',
 'scipy>=1.4.1']

entry_points = \
{'crowsetta.format': ['csv = crowsetta.csv',
                      'koumura = crowsetta.koumura',
                      'notmat = crowsetta.notmat',
                      'phn = crowsetta.phn',
                      'textgrid = crowsetta.textgrid']}

setup_kwargs = {
    'name': 'crowsetta',
    'version': '3.1.1.post1',
    'description': 'A tool to work with any format for annotating vocalizations',
    'long_description': "# crowsetta\n[![Build Status](https://github.com/NickleDave/crowsetta/actions/workflows/ci.yml/badge.svg)](https://github.com/NickleDave/crowsetta/actions)\n[![Documentation Status](https://readthedocs.org/projects/crowsetta/badge/?version=latest)](https://crowsetta.readthedocs.io/en/latest/?badge=latest)\n[![DOI](https://zenodo.org/badge/159904494.svg)](https://zenodo.org/badge/latestdoi/159904494)\n[![PyPI version](https://badge.fury.io/py/crowsetta.svg)](https://badge.fury.io/py/crowsetta)\n\n`crowsetta` is a tool to work with any format for annotating vocalizations: speech, birdsong, \nmouse ultrasonic calls (insert your favorite animal vocalization here).\n**The goal of** `crowsetta` **is to make sure that your ability to work with a dataset \nof vocalizations does not depend on your ability to work with any given format for \nannotating that dataset.** What `crowsetta` gives you is **not** yet another format for \nannotation (I promise!); instead you get some nice data types that make it easy to \nwork with any format: namely, `Sequence`s made up of `Segment`s.\n\n```Python\n    >>> from crowsetta import Segment, Sequence\n    >>> a_segment = Segment.from_keyword(\n    ...     label='a',\n    ...     onset_Hz=16000,\n    ...     offset_Hz=32000,\n    ...     file='bird21.wav'\n    ...     )\n    >>> list_of_segments = [a_segment] * 3\n    >>> seq = Sequence(segments=list_of_segments)\n    >>> print(seq)\n    Sequence(segments=[Segment(label='a', onset_s=None, offset_s=None, onset_Hz=16000, \n    offset_Hz=32000, file='bird21.wav'), Segment(label='a', onset_s=None, offset_s=None, \n    onset_Hz=16000, offset_Hz=32000, file='bird21.wav'), Segment(label='a', onset_s=None, \n    offset_s=None, onset_Hz=16000, offset_Hz=32000, file='bird21.wav')])\n```\n\nYou can load annotation from your format of choice into `Sequence`s of `Segment`s \n(most conveniently with the `Transcriber`, as explained below) and then use the \n`Sequence`s however you need to in your program.\n\nFor example, if you want to loop through the `Segment`s of each `Sequence`s to \npull syllables out of a spectrogram, you can do something like this, very Pythonically:\n\n```Python\n   >>> syllables_from_sequences = []\n   >>> for a_seq in seq:\n   ...     seq_dict = seq.to_dict()  # convert to dict with \n   ...     spect = some_spectrogram_making_function(seq['file'])\n   ...     syllables = []\n   ...     for seg in seq.segments:\n   ...         syllable = spect[:, seg.onset:seg.offset]  ## spectrogram is a 2d numpy array\n   ...         syllables.append(syllable)\n   ...     syllables_from_sequences.append(syllables)\n```\n\nAs mentioned above, `crowsetta` provides you with a `Transcriber` that comes equipped\nwith convenience functions to do the work of converting for you. \n\n```Python\n    from crowsetta import Transcriber\n    scribe = Transcriber()\n    seq = scribe.to_seq(file=notmat_files, format='notmat')\n```\n\nYou can even easily adapt the `Transcriber` to use your own in-house format, like so:\n\n```Python\n    from crowsetta import Transcriber\n    scribe = Transciber(user_config=your_config)\n    scribe.to_csv(file_'your_annotation_file.mat',\n                  csv_filename='your_annotation.csv')\n```\n\n## Features\n\n- convert annotation formats to `Sequence` objects that can be easily used in a Python program\n- convert `Sequence` objects to comma-separated value text files that can be read on any system\n- load comma-separated values files back into Python and convert to other formats\n- easily use with your own annotation format\n\nYou might find it useful in any situation where you want \nto share audio files of song and some associated annotations, \nbut you don't want to require the user to install a large \napplication in order to work with the annotation files.\n\n## Getting Started\nYou can install with pip:\n`$ pip install crowsetta`\n\nTo learn how to use `crowsetta`, please see the documentation at:  \n<https://crowsetta.readthedocs.io/en/latest/index.html>\n\n### Development Installation\n\nCurrently `crowsetta` is developed with `conda`.\nTo set up a development environment:\n```\n$ conda create crowsetta-dev\n$ conda create -n crowsetta-dev python=3.6 numpy scipy attrs\n$ conda activate crowsetta-dev\n$ $ pip install evfuncs koumura\n$ git clone https://github.com/NickleDave/crowsetta.git\n$ cd crowsetta\n$ pip install -e .\n```\n\n\n## Project Information\n\n### Background\n\n`crowsetta` was developed for two libraries:\n- `hybrid-vocal-classifier` <https://github.com/NickleDave/hybrid-vocal-classifier>\n- `vak` <https://github.com/NickleDave/vak>\n\nTesting relies on the `Vocalization Annotation Formats Dataset` which you may find useful if you need\nsmall samples of different audio files and associated annotation formats\n- on Figshare: <https://figshare.com/articles/Vocalization_Annotation_Formats_Dataset/8046920>\n- built from this GitHub repository: <https://github.com/NickleDave/vocal-annotation-formats>\n\n### Support\n\nIf you are having issues, please let us know.\n\n- Issue Tracker: <https://github.com/NickleDave/crowsetta/issues>\n\n### Contribute\n\n- Issue Tracker: <https://github.com/NickleDave/crowsetta/issues>\n- Source Code: <https://github.com/NickleDave/crowsetta>\n\n### CHANGELOG\nYou can see project history and work in progress in the [CHANGELOG](./doc/CHANGELOG.md)\n\n### License\n\nThe project is licensed under the [BSD license](./LICENSE).\n\n### Citation\nIf you use `crowsetta`, please cite the DOI:\n[![DOI](https://zenodo.org/badge/159904494.svg)](https://zenodo.org/badge/latestdoi/159904494)",
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickleDave/crowsetta',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
