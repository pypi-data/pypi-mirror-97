# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vak',
 'vak.cli',
 'vak.config',
 'vak.core',
 'vak.core.learncurve',
 'vak.datasets',
 'vak.engine',
 'vak.files',
 'vak.io',
 'vak.metrics',
 'vak.metrics.classification',
 'vak.metrics.distance',
 'vak.models',
 'vak.plot',
 'vak.split',
 'vak.split.algorithms',
 'vak.transforms']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3',
 'attrs>=19.3.0',
 'crowsetta>=3.1.1',
 'dask[bag]>=2.10.1',
 'evfuncs>=0.3.2',
 'joblib>=0.14.1',
 'matplotlib>=3.3.3',
 'numpy>=1.18.1',
 'pandas>=1.0.1',
 'scipy>=1.4.1',
 'tensorboard>=2.2.0',
 'toml>=0.10.2',
 'torch>=1.4.0,!=1.8.0',
 'torchvision>=0.5.0',
 'tqdm>=4.42.1']

entry_points = \
{'console_scripts': ['vak = vak.__main__:main'],
 'vak.metrics': ['Accuracy = vak.metrics.Accuracy',
                 'Levenshtein = vak.metrics.Levenshtein',
                 'SegmentErrorRate = vak.metrics.SegmentErrorRate']}

setup_kwargs = {
    'name': 'vak',
    'version': '0.4.0b1',
    'description': 'a neural network toolbox for animal vocalizations and bioacoustics',
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
