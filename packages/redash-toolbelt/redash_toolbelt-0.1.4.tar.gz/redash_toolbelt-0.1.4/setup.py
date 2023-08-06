# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redash_toolbelt', 'redash_toolbelt.examples']

package_data = \
{'': ['*'],
 'redash_toolbelt.examples': ['20210302_adventureclub_query_export/*']}

install_requires = \
['click>=7.0,<8.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['clone-dashboard-and-queries = '
                     'redash_toolbelt.examples.clone_dashboard_and_queries:main',
                     'export-queries = '
                     'redash_toolbelt.examples.query_export:main',
                     'find-tables = '
                     'redash_toolbelt.examples.find_table_names:main',
                     'gdpr-scrub = redash_toolbelt.examples.gdpr_scrub:lookup']}

setup_kwargs = {
    'name': 'redash-toolbelt',
    'version': '0.1.4',
    'description': 'Redash API client and tools to manage your instance.',
    'long_description': None,
    'author': 'Redash Maintainers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
