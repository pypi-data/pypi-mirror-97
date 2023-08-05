# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpeasy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'cryptography==3.4.5',
 'fire>=0.3.1,<0.4.0',
 'openshift-client==1.0.12',
 'sh>=1.14.1,<2.0.0',
 'simple-term-menu>=0.10.4,<0.11.0']

entry_points = \
{'console_scripts': ['ocpeasy = ocpeasy.__main__:cli']}

setup_kwargs = {
    'name': 'ocpeasy',
    'version': '0.1.17',
    'description': 'OCPeasy is an open-source software provisioning, configuration management, and application-deployment tool enabling infrastructure as code on OpenShift.',
    'long_description': '# OCPeasy - Command Line Interface\n\n![](https://github.com/ocpeasy/ocpeasy/workflows/ocpeasy-ubuntu-ci/badge.svg)\n[![Website shields.io](https://img.shields.io/website-up-down-green-red/https/www.ocpeasy.org)](https://www.ocpeasy.org/)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![PyPI download month](https://img.shields.io/pypi/dm/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)\n![](https://raw.githubusercontent.com/ocpeasy/ocpeasy/master/badges/coverage.svg)\n[![PyPI license](https://img.shields.io/pypi/l/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)\n[![PyPI version fury.io](https://badge.fury.io/py/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)\n\n\n## Introduction\n\nOCPeasy consists in a CLI to facilitate the deployment of OpenShift applications, generating the configuration based on your project requirements.\n\n## Pre-requisites (Development)\n\n- Poetry is required to develop and test locally the CLI.\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\n- pre-commit is required to ensure linting (with flake8) and formatting (with black) are applied before each commit\n\n`make config_precommit`\n\n## Get started\n\n### Prerequisites (end user):\n\n- `oc` corresponding to the version used by OpenShift server (https://docs.openshift.com/container-platform/4.1/release_notes/versioning-policy.html)\n<!-- - `curl`\n- `(Windows 10 only) WSL installed` -->\n\n### Appendix\n\nThe default install location is `~/.poetry/bin/poetry`\n\nI added the following to my `.zshrc`\n\n`export PATH=$PATH:$HOME/.poetry/bin`\n\n## Roadmap\n\n- [x] Configuring Tests/Linting\n- [x] Generate Project yaml `ocpeasy.yml`\n- [x] Generate Stage folder `<rootProject>/<.ocpeasy>/<stage>/[stagesFiles].yml`\n- [x] Supporting CLI invocation from `ocpeasy` directly\n- [ ] Supporting environment variables\n- [ ] Schema based validation\n- [ ] Composing existing stages with modules (e.g.: Databases, Caches, Messaging Queue, other applications etc...)\n- [ ] Support SSH Keys for cloning (read: https://stackoverflow.com/questions/28291909/gitpython-and-ssh-keys)\n\n## Examples\n\n### Pre-requisite\n\n- `oc login`\n\n### Multi-stage deployment\n\n- `ocpeasy scaffold`\n- `ocpeasy createStage` (create a new dev stage for your project)\n- `ocpeasy deploy --stageId=dev`\n- `ocpeasy createStage` (create a new prod stage for your project)\n- `ocpeasy deploy --stageId=prod`\n\n### Using OCPeasy behind a proxy\n\n- `ocpeasy scaffold --proxy=http://proxy.acme-corp.net:3450`\n\n## License\n\nCopyright 2021 ocpeasy\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'David Barrat',
    'author_email': 'david.barrat@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.ocpeasy.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
