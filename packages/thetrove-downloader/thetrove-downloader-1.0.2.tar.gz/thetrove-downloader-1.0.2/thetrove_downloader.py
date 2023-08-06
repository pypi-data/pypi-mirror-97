#!python3.9

from argparse import ArgumentParser
from argparse import Namespace
from json import dump
from json import load
from os import makedirs
from os import remove
from os.path import dirname
from os.path import isfile
from os.path import join
from platform import python_version
from platform import uname
from re import IGNORECASE
from re import Pattern
from re import compile as compile_pattern
from sys import argv
from sys import exit
from typing import Optional
from urllib.parse import quote
from urllib.parse import unquote
from urllib.parse import urljoin
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response
from requests import request
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TaskID
from rich.progress import TimeRemainingColumn
from rich.progress import TotalFileSizeColumn
from rich.theme import Theme
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

__version__: str = "1.0.2"
root: str = "https://thetrove.is"
user_agent: str = f"thetrove-downloader/{__version__} Python/{python_version()} {(u := uname()).system}/{u.release}"
download_flag: bool = True
blacklist: Optional[Pattern] = None
whitelist: Optional[Pattern] = None
progress_columns: list = [
    "[progress.description]{task.description}",
    TotalFileSizeColumn(),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.0f}%",
    TimeRemainingColumn(),
]
console: Console = Console(theme=Theme({
    "plain": "not bold default",
    "dim": "not bold dim default",
}))

disable_warnings(InsecureRequestWarning)


class NoRoot(Exception):
    pass


def print_indent(indent: int, message: str = "", style: str = ""):
    console.print("| " * (indent - 1), "|-" * bool(indent > 0 and message), f"[{style}]{message}[/{style}]", sep="")


def check_url(url: str) -> str:
    return request("GET", url, stream=True, headers={"User-Agent": user_agent}).request.url


def download_file(url: str, dest: str):
    try:
        with Progress(*progress_columns, transient=True) as progress:
            stream: Response = request("GET", url, stream=True, headers={"User-Agent": user_agent})
            size: int = int(stream.headers.get("Content-Length", 0))
            task: TaskID = progress.add_task("", total=size if size else 1)
            makedirs(dirname(dest), exist_ok=True)
            if not size:
                open(dest, "wb").write(stream.content)
            else:
                with open(dest, "wb") as f:
                    for chunk in stream.iter_content(chunk_size=1024):
                        f.write(chunk)
                        progress.advance(task, len(chunk))
            progress.advance(task, 1)
    except (Exception, BaseException) as err:
        remove(dest) if isfile(dest) else None
        raise err


def download(url: str, folder: str, output: str = ""):
    global download_flag, whitelist, blacklist

    output = output if output else unquote(url.strip("/").split("/")[-1])
    output = output.rstrip("/") + "/" * url.endswith("/")
    path: str = join(folder, output)
    path_url: str = unquote(urlparse(url).path)
    depth: int = folder.strip("/").count("/") + 1 if folder else 0

    if whitelist and not whitelist.search(path_url):
        print_indent(depth, output, "dim")
        return
    elif blacklist and blacklist.search(path_url):
        print_indent(depth, output, "dim")
        return

    print_indent(depth, output, "plain")

    if not url.endswith("/"):
        download_file(url, path) if download_flag and not isfile(path) else None
    else:
        res: Response = request("GET", url, verify=False, headers={"User-Agent": user_agent})
        page: BeautifulSoup = BeautifulSoup(res.text, "lxml")
        elements: list[Tag] = [a for td in page.findAll("td", {"class": "link"})[1:] for a in td.findAll("a")]
        for a in elements:
            download(urljoin(url, a["href"]), path)


def main(*args: str):
    global download_flag, whitelist, blacklist

    args_parser: ArgumentParser = ArgumentParser()

    args_parser.add_argument("-t, --target", dest="target", default="", required=False,
                             help="download target (folder or file)")
    args_parser.add_argument("-j, --json", dest="json", default="", required=False,
                             help="save/read instructions from a JSON file")
    args_parser.add_argument("-f, --folder", dest="folder", default="", required=False,
                             help="download destination folder")
    args_parser.add_argument("-o, --output", dest="output", default="", required=False,
                             help="output name of download target")
    args_parser.add_argument("-b, --blacklist", dest="blacklist", default="", required=False,
                             help="regex blacklist for files/folders")
    args_parser.add_argument("-w, --whitelist", dest="whitelist", default="", required=False,
                             help="regex whitelist for files/folders, overrides blacklist")
    args_parser.add_argument("--no-download", dest="no_download", default=False, action="store_true", required=False,
                             help="list content without downloading")
    args_parser.add_argument("--no-preserve-root", dest="no_preserve_root", default=False, action="store_true", required=False,
                             help="allow download of root folders")
    args_parser.add_argument("-v, --version", dest="version", default=False, action="store_true", required=False,
                             help="show version")

    args_parsed: Namespace = args_parser.parse_args(args)

    if all(not arg for arg in vars(args_parsed).values()):
        args_parser.print_help()
        exit(0)
    elif args_parsed.version:
        print(__version__)
        exit(0)
    elif not (args_parsed.target or args_parsed.json):
        args_parser.error("at least one of the following arguments is required: -t, --target, -j, --json")

    download_flag = not args_parsed.no_download

    instruction_new: dict[str, str] = {
        "target": args_parsed.target.removeprefix(root),
        "folder": args_parsed.folder,
        "output": args_parsed.output,
        "blacklist": args_parsed.blacklist,
        "whitelist": args_parsed.whitelist,
    } if args_parsed.target else {}
    instructions: list[dict[str, str]] = []

    if args_parsed.json:
        instructions = load(open(args_parsed.json, "r")) if isfile(args_parsed.json) else []
        if instruction_new and instruction_new not in instructions:
            instructions.append(instruction_new)
            instructions.sort(key=lambda i: i["target"])
            dump(instructions, open(args_parsed.json, "w"), indent=2)

    instructions = [instruction_new] if instruction_new else instructions

    for inst in instructions:
        console.print(inst) if len(instructions) > 1 else None
        whitelist = compile_pattern(inst["whitelist"], flags=IGNORECASE) if inst["whitelist"] else None
        blacklist = compile_pattern(inst["blacklist"], flags=IGNORECASE) if inst["blacklist"] else None
        target: str = check_url(urljoin(root, quote(inst["target"])))
        if not args_parsed.no_preserve_root and (d := urlparse(target).path.rstrip("/").count("/")) < 2:
            raise NoRoot(f"Cannot download targets with a depth lower than 2: {target} {d}")
        download(target, f if (f := inst["folder"]) else ".", inst["output"])
        print()


def __main__():
    try:
        main(*argv[1:])
    except KeyboardInterrupt:
        exit(130)
    except SystemExit as exit_:
        raise exit_
    except (Exception, BaseException):
        console.print_exception()


if __name__ == '__main__':
    __main__()
