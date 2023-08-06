# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cytopy',
 'cytopy.data',
 'cytopy.flow',
 'cytopy.flow.cell_classifier',
 'cytopy.flow.clustering',
 'cytopy.flow.plotting',
 'cytopy.tests']

package_data = \
{'': ['*'], 'cytopy.tests': ['assets/*']}

install_requires = \
['FlowIO==0.9.5',
 'KDEpy==1.0.10',
 'MiniSom>=2.2.6,<3.0.0',
 'PhenoGraph>=1.5.6,<2.0.0',
 'anytree>=2.8,<3.0',
 'autodocsumm>=0.2.1,<0.3.0',
 'cython>=0.29,<0.30',
 'detecta>=0.0.5,<0.0.6',
 'flowutils==0.9.1',
 'future>=0.18,<0.19',
 'graphviz>=0.14,<0.15',
 'h5py>=2.10,<3.0',
 'harmonypy==0.0.5',
 'hdbscan>=0.8,<0.9',
 'imbalanced-learn>=0.7,<0.8',
 'ipython>=7.18.1,<8.0.0',
 'matplotlib>=3.3,<4.0',
 'mongoengine>=0.20,<0.21',
 'nbconvert>=6.0,<7.0',
 'networkx>=2.5,<3.0',
 'oauthlib>=3.1.0,<4.0.0',
 'openpyxl==3.0.6',
 'pandas>=1.1.2,<2.0.0',
 'phate>=1.0.4,<2.0.0',
 'pingouin>=0.3.8,<0.4.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'scikit-fda==0.5',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.0,<2.0.0',
 'scprep>=1.0,<2.0',
 'seaborn>=0.11.0,<0.12.0',
 'setuptools>=49.6.0,<50.0.0',
 'shap==0.38.1',
 'shapely==1.7.1',
 'snowballstemmer>=2.0.0,<3.0.0',
 'statsmodels>=0.12,<0.13',
 'tables>=3.6.1,<4.0.0',
 'tensorflow>=2.4,<3.0',
 'tqdm>=4.49.0,<5.0.0',
 'umap-learn>=0.4.6,<0.5.0',
 'uncertainties>=3.1,<4.0',
 'xgboost>=1.2.0,<2.0.0',
 'xlrd>=1.2.0,<2.0.0',
 'yellowbrick>=1.1,<2.0']

setup_kwargs = {
    'name': 'cytopy',
    'version': '2.0',
    'description': 'Data centric algorithm agnostic cytometry analysis framework',
    'long_description': None,
    'author': 'Ross Burton',
    'author_email': 'burtonrj@cardiff.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
