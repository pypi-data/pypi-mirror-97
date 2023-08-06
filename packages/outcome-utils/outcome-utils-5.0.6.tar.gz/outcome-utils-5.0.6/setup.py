# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.utils', 'outcome.utils.bin', 'outcome.utils.jinja2']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.2.10,<4.0.0',
 'cachetools>=4.1.1,<5.0.0',
 'colored>=1.4.2,<2.0.0',
 'dogpile.cache>=1.0.2,<2.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'makefun>=1.9.3,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=6.2,<10.0',
 'semver>=2.10.2,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['otc-utils = outcome.utils.bin.otc_utils:main']}

setup_kwargs = {
    'name': 'outcome-utils',
    'version': '5.0.6',
    'description': 'A collection of python utils.',
    'long_description': "# utils-py\n![Continuous Integration](https://github.com/outcome-co/utils-py/workflows/Continuous%20Integration/badge.svg) ![version-badge](https://img.shields.io/badge/version-5.0.6-brightgreen)\n\nA set of python utilities.\n\n## Usage\n\n```sh\npoetry add outcome-utils\n```\n\n### Cache\n\nTo add cache to a module\n``` python\nfrom outcome.utils import cache\n\ncache_settings = {\n    '<your_prefix>.expiration': 300,  # Default\n    '<your_prefix>.backend': 'memory',  # Default\n}\n\nregion = cache.get_cache_region()\ncache.configure_cache_region(region, settings=cache_settings, prefix='<your_prefix>')\n```\n\nThen add to the functions to cache:\n``` python\n@region.cache_on_arguments()\ndef func_to_cache():\n    ...\n```\n\nOr for async functions:\n``` python\n@region.cache_on_arguments()\n@cache.cache_async\nasync def async_func_to_cache():\n    ...\n```\n\nTo have the cache persist on disk, specify the path\n``` python\nfrom pathlib import Path\n\ncache_settings = {\n    ...\n    '<your_prefix>.cache_path': f'{Path.home()}/.cache/example_path/cache.pkl'',\n    ...\n}\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n",
    'author': 'Douglas Willcocks',
    'author_email': 'douglas@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/utils-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
