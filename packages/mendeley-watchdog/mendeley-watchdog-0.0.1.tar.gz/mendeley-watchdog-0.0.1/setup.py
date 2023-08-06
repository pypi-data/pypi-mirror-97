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

"""Setup script"""

import os
import subprocess

from types import FunctionType
from typing import List, TextIO
from setuptools import find_packages, setup

from mendeley_watchdog.cli import mendeley

HEREDIR = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS_TXT = "requirements.txt"

PROG = "mendeley-watchdog"
DESC = "Distributes Mendeley bibtex file to specific destination upon change"
VERSION = "0.0.1"
GITHUB = "https://github.com/vlntnwbr/mendeley-watchdog"


def get_entrypoint(name: str, function: FunctionType) -> str:
    """Get setuptools entrypoint with name for function"""
    return "{}={}:{}".format(
        name, function.__module__, function.__name__
    )


def open_local(filename: str, mode: str = "r") -> TextIO:
    """Open file in this directory."""

    return open(os.path.join(HEREDIR, filename), mode)


def execute_command(args: List[str]) -> List[str]:
    """Execute external command and return stdout"""

    try:
        process = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return [line.strip() for line in process.stdout.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def create_requirements_txt() -> None:
    """Create file 'requirements.txt' from 'Pipfile.lock'."""

    try:
        with open_local("Pipfile.lock"):
            pass
    except FileNotFoundError:
        return

    pipenv_lines = execute_command(["pipenv", "lock", "-r"])
    if not pipenv_lines:
        return

    reqs = [line for line in pipenv_lines[1:] if line]
    with open_local(REQUIREMENTS_TXT, "w") as req_file:
        req_file.write("\n".join(reqs) + "\n")


def read_requirements() -> List[str]:
    """Read lines of requirements.txt and return them as list"""

    with open_local(REQUIREMENTS_TXT) as req_file:
        return [
            line.strip() for line in req_file.readlines()
            if line.strip() and not line.startswith("-i")
        ]


if __name__ == '__main__':
    create_requirements_txt()
    README = open_local("README.md").read()
    REQUIREMENTS = read_requirements()
    INSTALL_REQUIRES = REQUIREMENTS if REQUIREMENTS else None
    setup(
        name=PROG,
        description=DESC,
        version=VERSION,
        long_description=README,
        long_description_content_type="text/markdown",
        install_requires=INSTALL_REQUIRES,
        packages=find_packages(),
        include_package_data=True,
        url=GITHUB,
        author="Valentin Weber",
        author_email="dev@vweber.eu",
        license="EUPL v1.2 or later",
        project_urls={
            "Bug Tracker": GITHUB + "/issues",
            "Documentation": GITHUB + f"/tree/v{VERSION}/docs"
        },
        entry_points={"console_scripts": [
            get_entrypoint(mendeley.NAME, mendeley.main)
        ]},
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3 :: Only",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Topic :: System :: Filesystems",
            "Topic :: System :: Monitoring",
            "Topic :: Utilities",
            "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)"  # noqa pylint: disable=line-too-long
        ]
    )
