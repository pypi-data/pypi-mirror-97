# thetrove-downloader

[![version_pypi](https://img.shields.io/pypi/v/thetrove-downloader?logo=pypi)](https://pypi.org/project/thetrove-downloader/)
[![version_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=gitlab&query=%24%5B%3A1%5D.name&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Fthetrove-downloader%2Frepository%2Ftags)](https://gitlab.com/MatteoCampinoti94/thetrove-downloader)
[![version_python](https://img.shields.io/pypi/pyversions/thetrove-downloader?logo=Python)](https://www.python.org)

[![issues_gitlab](https://img.shields.io/badge/dynamic/json?logo=gitlab&color=orange&label=issues&suffix=%20open&query=%24.length&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2Fmatteocampinoti94%252Fthetrove-downloader%2Fissues%3Fstate%3Dopened)](https://gitlab.com/MatteoCampinoti94/thetrove-downloader/issues)


This Python package allows to easily download any resource, be it folder or file, from [The Trove.is](https://thetrove.is).

## Installation and Requirements

The program requires Python 3.9 or above.

To install the program it is sufficient to use Python pip and get the package `thetrove-downloader`. The package will add a new command `thetrove-downloader`.

```shell
python3 -m pip install thetrove-downloader
```

Updates should be performed via pip.

```shell
python3 -m pip install --upgrade thetrove-downloader
```

## Usage

```shell
thetrove-downloader [-h] [-t, --target TARGET] [-j, --json JSON]
                           [-f, --folder FOLDER] [-o, --output OUTPUT]
                           [-b, --blacklist BLACKLIST]
                           [-w, --whitelist WHITELIST] [--no-download]
                           [--no-preserve-root]
```

* `-h, --help` show help message

* `-t, --target <TARGET>` download target (folder or file)<br>
  To download a specific resource, start the program with the `--target` command and supply a valid path (e.g. "Books/White Star").

* `-j, --json <JSON>` save/read instructions from a JSON file<br>
  The `--json` option allows to specify a file to save the target, folder, output, whitelist, and blacklist instructions in JSON format. Launching the program with only the `--json` option will load the instructions previously saved in the file and perform all of them in succession. This can be used to keep a local copy of specific resources up to date.

* `-f, --folder <FOLDER>` destination folder<br>
  The `--folder` option allows to specify a folder in which the targeted resource will be downloaded.

* `-o, --output <OUTPUT>` output name of download target<br>
  The `--output` option allows to override the folder/file name of the resource. Note that if the targeted resource is a folder, the option will only apply to the top-level folder and leave all contents therein unaltered.

* `-b, --blacklist <BLACKLIST>` regex blacklist for files/folders<br>
  The `--whitelist` option allows to specify a regex pattern that will be used to skip files and folder that do not contain the supplied pattern. Overwrites blacklist options.

* `-w, --whitelist <WHITELIST>` regex whitelist for files/folders, overrides blacklist<br>
  The `--whitelist` option allows to specify a regex pattern that will be used to skip files and folder that do not contain the supplied pattern. Overwrites blacklist options.

* `--no-download` list content without downloading<br>
  The `--no-download` flag allows to list the content under the supplied target without performing any download. The instructions will still be saved in a JSON file if the `--json` options is used, but not the flag.
  
* `--no-preserve-root` allow download of root folders<br>
  The `--no-preserve-root` flag allows downloading entire root folders such as "/Books/". This flag is not preserved with the `--json` option and must be passed manually every time.

_**NOTE**_: the program requires to use either `--target`, `--json`, or both `--target` and `--json`. Without one of these combinations the program won't have a valid download instruction.

## Notes on Crawling

The program performs all GET requests without throttling or delay and with no disallowed paths as per the instructions at [thetrove.is/robots.txt](https://thetrove.is/robots.txt).

However, please do take care to not overuse this utility and risk overwhelming their connection. Thank you.

Root folders such as "/Books" are protected and cannot be downloaded without using the `--no-preserve-root` flag.