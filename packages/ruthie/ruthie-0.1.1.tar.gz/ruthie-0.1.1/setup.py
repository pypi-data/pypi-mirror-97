# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruthie', 'ruthie.commands', 'ruthie.toolset']

package_data = \
{'': ['*']}

install_requires = \
['docopt==0.6.2', 'toml>=0.9,<0.10', 'xmlrunner>=1.7.7,<1.8.0']

entry_points = \
{'console_scripts': ['ruthie = =ruthie.cli:main']}

setup_kwargs = {
    'name': 'ruthie',
    'version': '0.1.1',
    'description': 'Run Unit Tests Harmoniously Incredibly Easy',
    'long_description': '# ruthie\n\n[![Current Release](https://img.shields.io/github/release/bitbar/ruthie.svg)](releases)\n[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE.md)\n\nRun Unit Tests Harmoniously Incredibly Easy\n\nThis repo contains _ruthie_ which is the Unittests runner.\n\n## Installation\n\nTODO\n\n## Usage\n\nTODO\n\n## License\n\nThis project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.\n',
    'author': 'Marek Sierociński',
    'author_email': 'marek.sierocinski@smartbear.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bitbar/ruthie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
