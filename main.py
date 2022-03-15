import os
import sys
from pyupdater.client import Client
from toml import load
import argparse

from client_config import ClientConfig

poetry_config = load("pyproject.toml")

APP_VERSION = poetry_config["tool"]["poetry"]["version"]


def parse_args(argv):
    usage = "%(prog)s [options]\n"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("--version", action="store_true", help="displays version")
    parser.add_argument(
        "integers",
        metavar="N",
        type=int,
        nargs="+",
        help="an integer for the accumulator",
    )

    return parser.parse_args(argv[1:])


def display_version_and_exit():
    """
    Display version and exit.
    In some versions of PyInstaller, sys.exit can result in a
    misleading 'Failed to execute script run' message which
    can be ignored: https://github.com/pyinstaller/pyinstaller/commit/36b6ab30b11dbe2a9b505c1bb415ead10ec8a66f
    """
    sys.stdout.write(APP_VERSION)
    sys.exit(0)


def print_status_info(info):
    total = info.get("total")
    downloaded = info.get("downloaded")
    status = info.get("status")
    print(downloaded, total, status)


def check_for_updates():
    client = Client(ClientConfig(), refresh=True, progress_hooks=[print_status_info])
    app_update = client.update_check(ClientConfig.APP_NAME, APP_VERSION)

    if app_update:
        if getattr(sys, "frozen", False):
            downloaded = app_update.download()
            if downloaded:
                print("Extracting update and restarting")
                app_update.extract_restart()
            else:
                print("Download failed")
        else:
            print("Update available but app not frozen")
    else:
        print("no updates available")


if __name__ == "__main__":
    args = parse_args(sys.argv)
    if args.version:
        display_version_and_exit()

    check_for_updates()

    total_args = len(args.integers)
    print("Total arguments passed:", total_args)
    print(f"\nArguments passed: {args}\n")
