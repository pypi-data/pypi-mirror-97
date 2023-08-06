# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt', 'dbt.adapters.ibmdb2', 'dbt.include.ibmdb2']

package_data = \
{'': ['*'],
 'dbt.include.ibmdb2': ['macros/*',
                        'macros/materializations/incremental/*',
                        'macros/materializations/seed/*',
                        'macros/materializations/snapshot/*']}

install_requires = \
['dbt-core>=0.19,<0.20', 'ibm-db>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'dbt-ibmdb2',
    'version': '0.1.0',
    'description': 'The db2 adapter plugin for dbt (data build tool)',
    'long_description': None,
    'author': 'aurany',
    'author_email': 'rasmus.nyberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
