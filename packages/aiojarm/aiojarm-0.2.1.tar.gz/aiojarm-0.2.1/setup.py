# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiojarm']

package_data = \
{'': ['*']}

install_requires = \
['aiometer>=0.2.1,<0.3.0',
 'poetry-version>=0.1.5,<0.2.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.7.0,<4.0.0']}

entry_points = \
{'console_scripts': ['aiojarm = aiojarm.cli:main_wrapper']}

setup_kwargs = {
    'name': 'aiojarm',
    'version': '0.2.1',
    'description': 'Async JARM client',
    'long_description': '# aiojarm\n\n![CI](https://github.com/ninoseki/aiojarm/workflows/CI/badge.svg)\n![Python versions](https://img.shields.io/pypi/pyversions/aiojarm.svg)\n[![PyPI version](https://badge.fury.io/py/aiojarm.svg)](https://badge.fury.io/py/aiojarm)\n\nAsync version of [JARM](https://github.com/salesforce/jarm).\n\n## Installation\n\n```bash\npip install aiojarm\n```\n\n## Usage\n\n```python\nimport asyncio\nimport aiojarm\n\nloop = asyncio.get_event_loop()\nfingerprints = loop.run_until_complete(\n    asyncio.gather(\n        aiojarm.scan("www.salesforce.com"),\n        aiojarm.scan("www.google.com"),\n        aiojarm.scan("www.facebook.com"),\n        aiojarm.scan("github.com"),\n    )\n)\nprint(fingerprints)\n# [\n#     (\n#         "www.salesforce.com",\n#         443,\n#         "23.42.156.194",\n#         "2ad2ad0002ad2ad00042d42d00000069d641f34fe76acdc05c40262f8815e5",\n#     ),\n#     (\n#         "www.google.com",\n#         443,\n#         "172.217.25.228",\n#         "27d40d40d29d40d1dc42d43d00041d4689ee210389f4f6b4b5b1b93f92252d",\n#     ),\n#     (\n#         "www.facebook.com",\n#         443,\n#         "31.13.82.36",\n#         "27d27d27d29d27d1dc41d43d00041d741011a7be03d7498e0df05581db08a9",\n#     ),\n#     (\n#         "github.com",\n#         443,\n#         "52.192.72.89",\n#         "29d29d00029d29d00041d41d0000008aec5bb03750a1d7eddfa29fb2d1deea",\n#     ),\n# ]\n```\n\n## CLI usage\n\n```bash\n$ aiojarm --help\nUsage: aiojarm [OPTIONS] HOSTNAMES...\n\nArguments:\n  HOSTNAMES...  IPs/domains or a file which contains a list of IPs/domains per\n                line  [required]\n\n\nOptions:\n  --port INTEGER         [default: 443]\n  --max-at-once INTEGER  [default: 8]\n  --install-completion   Install completion for the current shell.\n  --show-completion      Show completion for the current shell, to copy it or\n                         customize the installation.\n\n  --help                 Show this message and exit.\n\n$ aiojarm 1.1.1.1\n1.1.1.1,443,1.1.1.1,27d3ed3ed0003ed1dc42d43d00041d6183ff1bfae51ebd88d70384363d525c\n\n$ aiojarm google.com.ua google.gr\ngoogle.com.ua,443,172.217.25.195,27d40d40d29d40d1dc42d43d00041d4689ee210389f4f6b4b5b1b93f92252d\ngoogle.gr,443,216.58.220.131,27d40d40d29d40d1dc42d43d00041d4689ee210389f4f6b4b5b1b93f92252d\n\n# or you can input hostnames via a file\n$ aiojarm list.txt\n```\n\n## License\n\nJARM is created by Salesforce\'s JARM team and it is licensed with 3-Clause "New" or "Revised" License.\n\n- https://github.com/salesforce/jarm/blob/master/LICENSE.txt\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
