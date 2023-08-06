# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biolib',
 'biolib.biolib_binary_format',
 'biolib.pyppeteer.docs',
 'biolib.pyppeteer.pyppeteer',
 'biolib.pyppeteer.pyppeteer.connection',
 'biolib.pyppeteer.pyppeteer.frame',
 'biolib.pyppeteer.pyppeteer.models',
 'biolib.pyppeteer.utils']

package_data = \
{'': ['*'],
 'biolib': ['biolib-js/*', 'pyppeteer/*', 'pyppeteer/.circleci/*'],
 'biolib.pyppeteer.docs': ['_static/*', '_templates/*']}

install_requires = \
['aenum>=2.2.3,<3.0.0',
 'appdirs>=1.4.3,<2.0.0',
 'certifi>=2019.11.28',
 'docker==4.4.1',
 'nest_asyncio==1.4.0',
 'ordered_set>=4.0.1,<5.0.0',
 'pyee>=7.0.1,<8.0.0',
 'pyyaml==5.4.1',
 'requests==2.24.0',
 'tqdm>=4.42.1,<5.0.0',
 'websockets>=8.1,<9.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0',
                             'typing_inspect>=0.5.0,<0.6.0']}

entry_points = \
{'console_scripts': ['biolib = biolib:cli']}

setup_kwargs = {
    'name': 'pybiolib',
    'version': '0.1.733',
    'description': 'BioLib Python Client',
    'long_description': '# PyBioLib\n\nPyBioLib is a Python package for running BioLib applications from Python scripts, and the command line.\n\n### Python Example\n```python\n# pip3 install pybiolib\nfrom biolib.samtools import samtools\nresult = samtools()\nprint(result.stdout)\n```\n\n### Command Line Example\n```bash\npip3 install pybiolib\nbiolib run samtools/samtools\n```\n',
    'author': 'biolib',
    'author_email': 'hello@biolib.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/biolib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
