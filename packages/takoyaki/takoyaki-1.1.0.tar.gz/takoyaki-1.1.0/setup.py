# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['takoyaki', 'takoyaki.cli', 'takoyaki.sute']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'colorama>=0.4.4,<0.5.0',
 'questionary>=1.9.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typing>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['tako = takoyaki.cli.tako:main']}

setup_kwargs = {
    'name': 'takoyaki',
    'version': '1.1.0',
    'description': 'Instant burner mail account creation and management script.',
    'long_description': '<p align="center">\n  <img src="https://u.teknik.io/00UzK.svg">\n</p>\n\n# Takoyaki [![GitHub release (latest by date)](https://img.shields.io/github/v/release/kebablord/takoyaki?style=flat-square)](https://github.com/kebablord/takoyaki/releases/latest)  [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kebablord/takoyaki/Check%20errors%20and%20lint?style=flat-square)](https://github.com/KebabLord/takoyaki/actions) [![Pypi version](https://img.shields.io/pypi/v/takoyaki?style=flat-square)](https://pypi.org/project/takoyaki/)\nTakoyaki is a simple tool to create random/burner instant mails and generate registration credentials. It\'s simply cli version of m.kuku.lu service and a cli frontend to sute-mail-python module.\n\n### Installation & Usage\nYou can simply install it from pypi\n```pip install takoyaki```\nYou can also download the prebuilt binaries from [releases](https://github.com/KebabLord/takoyaki/releases) or run the script directly from `tako` symlink after installing dependencies with `pip3 install -r requirements.txt`.\n### Usage\n```λ ./takoyaki.py -h\nTakoyaki is an interactive burner mail creator and controller.\nUsage:\n  takoyaki [COMMAND] [ARGS...]\n  takoyaki -h | --help\n\nCommands:\n  create [-h]               Create new random mail address\n  read   [-hal]             Read mails from specified address\n  wait   [-ha]              Wait for new mails on specified address\n  del    [-ha]              Delete specified mail address\n  list   [-h]               List current mail addresses\n  gen    [-hwpusa]          Generate registration details\n\nOptions:\n  -h, --help                Show extended information about the subcommand\n  -a, --address <ADDRESS>   Specify the mail address\n  -l, --last                Select latest mail\n  -p, --password            Generate password\n  -u, --uname               Generate username\n  -w, --Wait                Start listening new mails after generate (for verification mails)\n  -s, --save <NAME>         Save generated info to .accs file\n```\n### Examples:\n```\n# Create a new random instant mail address\n$ ./takoyaki create\ncreated: penanegya@mirai.re\n\n# List existing addresses\n$ ./takoyaki list\n1  misukedo@via.tokyo.jp\n2  kyakidokya@eay.jp\n3  penanegya@mirai.re\n\n# Let\'s read mails on the kyakidokya@eay.jp\n./takoyaki read -a kyaki\n> No mails.\n# or you can also specify index of address\n./takoyaki read -a 2\n> No mails.\n\n# Let\'s create a burner account for a gaming site,\n# generate a random password and a username,\n# save the credentials we generated to .accs file and wait for the verification mail.\n./takoyaki gen -a1 -puws "some name"\nor the long version;\n./takoyaki gen --address 1 --uname --password --wait --save="some name"\n=== Some Name Account ===\nMail: misukedo@via.tokyo.jp\nNick: jturlj74 \nPass: v0OEksf7.maiVdJ \n\nWaiting new mails for misukedo@via.tokyo.jp\nPress Ctrl+C to Abort.\n```\n\n',
    'author': 'Junicchi',
    'author_email': 'junicchi@waifu.club',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kebablord/takoyaki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
