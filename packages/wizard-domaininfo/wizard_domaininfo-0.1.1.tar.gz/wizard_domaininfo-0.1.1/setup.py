# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wizard_domaininfo']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'contextvars>=2.4,<3.0',
 'immutables>=0.15,<0.16',
 'importlib-metadata>=3.7.0,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'setuptools>=54.1.0,<55.0.0',
 'tomlkit>=0.7.0,<0.8.0',
 'typing>=3.7.4,<4.0.0',
 'wheel>=0.36.2,<0.37.0',
 'wizard-whois>=2.5.9,<3.0.0',
 'zipp>=3.4.1,<4.0.0']

entry_points = \
{'console_scripts': ['wizard-domaininfo = wizard_domaininfo.cli:main']}

setup_kwargs = {
    'name': 'wizard-domaininfo',
    'version': '0.1.1',
    'description': 'DNS/Whois Domain Information library',
    'long_description': '# Wizard Domaininfo\n\n[![pipeline status](https://gitlab.com/mikeramsey/wizard-domaininfo/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/wizard-domaininfo/pipelines)\n[![coverage report](https://gitlab.com/mikeramsey/wizard-domaininfo/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/wizard-domaininfo/commits/master)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/wizard-domaininfo/)\n[![pypi version](https://img.shields.io/pypi/v/wizard-domaininfo.svg)](https://pypi.org/project/wizard-domaininfo/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/wizard-domaininfo/community)\n\nDNS/Whois Domain Information library\n\n## Requirements\n\nWizard Domaininfo requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install wizard_domaininfo\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 wizard_domaininfo\n```\n',
    'author': 'Michael Ramsey',
    'author_email': 'mike@hackerdise.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mikeramsey/wizard-domaininfo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
