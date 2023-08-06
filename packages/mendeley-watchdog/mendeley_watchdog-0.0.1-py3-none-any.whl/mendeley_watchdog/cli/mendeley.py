##
#   Copyright (c) 2021 Valentin Weber
#
#   This file is part of the software mendeley-watchdog.
#
#   The software is licensed under the European Union Public License
#   (EUPL) version 1.2 or later. You should have received a copy of
#   the english license text with the software. For your rights and
#   obligations under this license refer to the file LICENSE or visit
#   https://joinup.ec.europa.eu/community/eupl/og_page/eupl to view
#   official translations of the licence in another language of the EU.
##

"""Entrypoint for Mendeley Watchdog intended for VS Code tasks"""

import argparse
import logging
import os

from ..main import Watchdog
from ..core.utils import append_file_ext, isdir, setup_logging

NAME = "mendeley-watchdog"
DESC = "watch BibTeX file and mirror its contents after modification"


class MendeleyWatchdog(argparse.ArgumentParser):
    """Command Line Parser"""

    def __init__(self):

        epilog = \
            "--mendeley-bibtex defaults to the value of the environment " \
            "variable MENDELEY_BIBTEX_DIR. If that isn't set and no value is" \
            " provided the program will exit."

        super().__init__(
            prog=NAME,
            description=DESC,
            epilog=epilog
        )

        self.add_argument(
            "--mendeley-bibtex",
            metavar="",
            dest="bibtex_dir",
            help="path to directory in which Mendeley stores BibTeX files",
            default=os.getenv("MENDELEY_BIBTEX", ""),
            type=self.existing_dir_arg
        )

        self.add_argument(
            "bibfile",
            help="name of mendeley bib file to watch",
        )
        self.add_argument(
            "mirrored",
            help="path to file Mendeley bib file mirrored will be mirrored to",
            type=self.writable_file_arg
        )

    @staticmethod
    def existing_dir_arg(value: str) -> str:
        """ArgumentTypeError if value doesn't point to directory"""

        checked_path = isdir(value)
        if not checked_path:
            raise argparse.ArgumentTypeError(f"directory not found: '{value}'")
        return value

    @staticmethod
    def writable_file_arg(value: str) -> str:
        """ArgumentTypeError if value doesn't point to writable file"""

        dirname, filename = os.path.split(value)
        checked_dir = isdir(dirname)
        if not checked_dir:
            raise argparse.ArgumentTypeError(f"directory not found: '{value}'")

        normed_path = os.path.join(checked_dir, filename)
        try:
            err = f"file not writable: '{normed_path}'"
            with open(normed_path, "ab"):
                pass
        except PermissionError as exc:
            raise argparse.ArgumentTypeError(err) from exc
        return normed_path


def main() -> None:
    """Run mendeley-watchdog"""

    setup_logging(f".{NAME}.log")
    log = logging.getLogger(NAME)

    cmd = MendeleyWatchdog()
    args = cmd.parse_args()
    file_to_watch, file_mirror = append_file_ext(
        args.bibfile, args.mirrored, f_ext=("bib", "bib")
    )
    log.info("watching '%s' in '%s'", file_to_watch, args.bibtex_dir)
    log.debug("file_mirror = '%s'", file_mirror)

    observer = Watchdog({
        "interval": 1,
        "bib_dir": args.bibtex_dir,
        "files": [(file_to_watch, file_mirror)]
    })
    observer.run()


if __name__ == "__main__":
    main()
