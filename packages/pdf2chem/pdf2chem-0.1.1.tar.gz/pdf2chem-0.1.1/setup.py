# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pdf2chem']
install_requires = \
['CIRpy>=1.0.2,<2.0.0',
 'ChemDataExtractor>=1.3.0,<2.0.0',
 'DateTime>=4.3,<5.0',
 'pandas>=1.2.3,<2.0.0',
 'textract>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'pdf2chem',
    'version': '0.1.1',
    'description': 'A curator for chemistry-related pdf files',
    'long_description': None,
    'author': 'johngoeltz',
    'author_email': '80011540+johngoeltz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
