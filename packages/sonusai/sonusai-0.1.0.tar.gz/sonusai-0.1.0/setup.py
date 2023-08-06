# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sonusai']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'h5py>=3.1.0,<4.0.0',
 'matplotlib>=3.3.1,<4.0.0',
 'sklearn>=0.0,<0.1',
 'sox>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'sonusai',
    'version': '0.1.0',
    'description': 'Framework for building deep neural network models for sound, speech, and voice AI',
    'long_description': 'Sonus AI: Framework for creating deep NN models for sound, speech, and voice AI\n',
    'author': 'Chris Eddington',
    'author_email': 'chris@aaware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
