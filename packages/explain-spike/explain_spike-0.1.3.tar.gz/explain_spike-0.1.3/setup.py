# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['explain_spike']

package_data = \
{'': ['*'], 'explain_spike': ['.ipynb_checkpoints/*']}

install_requires = \
['alibi>=0.5.5,<0.6.0',
 'dalex>=1.0.0,<2.0.0',
 'lightgbm>=3.1.1,<4.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'shap>=0.38.1,<0.39.0']

setup_kwargs = {
    'name': 'explain-spike',
    'version': '0.1.3',
    'description': 'Package that contains several methods and functions for explaining and understanding machine learning models',
    'long_description': None,
    'author': 'Javier Molina Ferreiro',
    'author_email': 'javier@spikelab.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
