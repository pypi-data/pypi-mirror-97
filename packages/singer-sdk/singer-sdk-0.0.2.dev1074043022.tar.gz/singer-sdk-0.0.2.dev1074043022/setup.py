# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['singer_sdk',
 'singer_sdk.helpers',
 'singer_sdk.samples.sample_tap_countries',
 'singer_sdk.samples.sample_tap_gitlab',
 'singer_sdk.samples.sample_tap_google_analytics',
 'singer_sdk.samples.sample_tap_parquet',
 'singer_sdk.samples.sample_tap_snowflake',
 'singer_sdk.streams',
 'singer_sdk.tests']

package_data = \
{'': ['*'],
 'singer_sdk.samples.sample_tap_countries': ['schemas/*'],
 'singer_sdk.samples.sample_tap_gitlab': ['schemas/*'],
 'singer_sdk.samples.sample_tap_google_analytics': ['resources/*', 'schemas/*'],
 'singer_sdk.tests': ['.secrets/*', 'resources/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'PyJWT==1.7.1',
 'backoff==1.8.0',
 'click>=7.1.2,<8.0.0',
 'cryptography>=3.4.6,<4.0.0',
 'pendulum==1.2.0',
 'pyarrow>=2.0.0,<3.0.0',
 'python-dateutil>=2.1,<2.8.1',
 'pytz==2018.4',
 'requests>=2.25.1,<3.0.0',
 'singer-python==5.9.0']

entry_points = \
{'console_scripts': ['plugin-base = singer_sdk.plugin_base:PluginBase.cli']}

setup_kwargs = {
    'name': 'singer-sdk',
    'version': '0.0.2.dev1074043022',
    'description': 'An open framework for building singer-compliant taps',
    'long_description': None,
    'author': 'Meltano Team and Contributors',
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
