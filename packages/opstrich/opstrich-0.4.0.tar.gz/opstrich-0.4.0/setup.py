# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opstrich', 'opstrich.invoke']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'invoke>=1.4.1,<2.0.0',
 'isort>=5.0,<6.0',
 'pyupgrade>=2.7.4,<3.0.0']

setup_kwargs = {
    'name': 'opstrich',
    'version': '0.4.0',
    'description': 'DevOps tooling, various scripts, etc.',
    'long_description': '# Opstrich\n#### DevOps tooling, various scripts, etc.\n\n![CI](https://github.com/RevolutionTech/opstrich/actions/workflows/ci.yml/badge.svg)\n\n## Installation\n\nFirst install the `opstrich` package:\n\n    pip install opstrich\n\nTo use the provided [invoke](http://www.pyinvoke.org/) tasks, you will also need to add these to a collection in your project:\n\n    # tasks.py\n\n    from invoke import Collection\n    from opstrich.invoke import check, openssl, package\n\n    namespace = Collection(check, openssl, package)\n\n## Usage\n\nOnce the invoke tasks have been added, you can view help information on them via `inv -l` and `inv --help`.\n',
    'author': 'Lucas Connors',
    'author_email': 'lucas@revolutiontech.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RevolutionTech/opstrich',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
