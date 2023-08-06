# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crowsetta']

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
    'version': '3.1.1',
    'description': 'A tool to work with any format for annotating vocalizations',
    'long_description': None,
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
