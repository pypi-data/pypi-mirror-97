# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xchk_mysql_comparison_strategies']

package_data = \
{'': ['*'],
 'xchk_mysql_comparison_strategies': ['solutions/*',
                                      'submitted_files/*',
                                      'templates/xchk_mysql_comparison_strategies/*']}

setup_kwargs = {
    'name': 'xchk-mysql-comparison-strategies',
    'version': '0.0.2',
    'description': 'Checks and strategies for comparing MySQL databases',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincentnys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
