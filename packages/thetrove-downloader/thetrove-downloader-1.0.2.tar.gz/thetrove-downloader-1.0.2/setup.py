# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['thetrove_downloader']
install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.5.2,<5.0.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=9.6.1,<10.0.0',
 'urllib3>=1.25.10,<2.0.0']

entry_points = \
{'console_scripts': ['thetrove-downloader = thetrove_downloader:__main__']}

setup_kwargs = {
    'name': 'thetrove-downloader',
    'version': '1.0.2',
    'description': 'Download utility for thetrove.is',
    'long_description': '# thetrove-downloader\n\n[![version_pypi](https://img.shields.io/pypi/v/thetrove-downloader?logo=pypi)](https://pypi.org/project/thetrove-downloader/)\n[![version_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=gitlab&query=%24%5B%3A1%5D.name&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Fthetrove-downloader%2Frepository%2Ftags)](https://gitlab.com/MatteoCampinoti94/thetrove-downloader)\n[![version_python](https://img.shields.io/pypi/pyversions/thetrove-downloader?logo=Python)](https://www.python.org)\n\n[![issues_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=issues&suffix=%20open&query=%24.length&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Fthetrove-downloader%2Fissues%3Fstate%3Dopened)](https://gitlab.com/MatteoCampinoti94/thetrove-downloader/issues)\n\n\nThis Python package allows to easily download any resource, be it folder or file, from [The Trove.is](https://thetrove.is).\n\n## Installation and Requirements\n\nThe program requires Python 3.9 or above.\n\nTo install the program it is sufficient to use Python pip and get the package `thetrove-downloader`. The package will add a new command `thetrove-downloader`.\n\n```shell\npython3 -m pip install thetrove-downloader\n```\n\nUpdates should be performed via pip.\n\n```shell\npython3 -m pip install --upgrade thetrove-downloader\n```\n\n## Usage\n\n```shell\nthetrove-downloader [-h] [-t, --target TARGET] [-j, --json JSON]\n                           [-f, --folder FOLDER] [-o, --output OUTPUT]\n                           [-b, --blacklist BLACKLIST]\n                           [-w, --whitelist WHITELIST] [--no-download]\n                           [--no-preserve-root]\n```\n\n* `-h, --help` show help message\n\n* `-t, --target <TARGET>` download target (folder or file)<br>\n  To download a specific resource, start the program with the `--target` command and supply a valid path (e.g. "Books/White Star").\n\n* `-j, --json <JSON>` save/read instructions from a JSON file<br>\n  The `--json` option allows to specify a file to save the target, folder, output, whitelist, and blacklist instructions in JSON format. Launching the program with only the `--json` option will load the instructions previously saved in the file and perform all of them in succession. This can be used to keep a local copy of specific resources up to date.\n\n* `-f, --folder <FOLDER>` destination folder<br>\n  The `--folder` option allows to specify a folder in which the targeted resource will be downloaded.\n\n* `-o, --output <OUTPUT>` output name of download target<br>\n  The `--output` option allows to override the folder/file name of the resource. Note that if the targeted resource is a folder, the option will only apply to the top-level folder and leave all contents therein unaltered.\n\n* `-b, --blacklist <BLACKLIST>` regex blacklist for files/folders<br>\n  The `--whitelist` option allows to specify a regex pattern that will be used to skip files and folder that do not contain the supplied pattern. Overwrites blacklist options.\n\n* `-w, --whitelist <WHITELIST>` regex whitelist for files/folders, overrides blacklist<br>\n  The `--whitelist` option allows to specify a regex pattern that will be used to skip files and folder that do not contain the supplied pattern. Overwrites blacklist options.\n\n* `--no-download` list content without downloading<br>\n  The `--no-download` flag allows to list the content under the supplied target without performing any download. The instructions will still be saved in a JSON file if the `--json` options is used, but not the flag.\n  \n* `--no-preserve-root` allow download of root folders<br>\n  The `--no-preserve-root` flag allows downloading entire root folders such as "/Books/". This flag is not preserved with the `--json` option and must be passed manually every time.\n\n_**NOTE**_: the program requires to use either `--target`, `--json`, or both `--target` and `--json`. Without one of these combinations the program won\'t have a valid download instruction.\n\n## Notes on Crawling\n\nThe program performs all GET requests without throttling or delay and with no disallowed paths as per the instructions at [thetrove.is/robots.txt](https://thetrove.is/robots.txt).\n\nHowever, please do take care to not overuse this utility and risk overwhelming their connection. Thank you.\n\nRoot folders such as "/Books" are protected and cannot be downloaded without using the `--no-preserve-root` flag.',
    'author': 'Matteo Campinoti',
    'author_email': 'matteo.campinoti94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/MatteoCampinoti94/thetrove-downloader',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
