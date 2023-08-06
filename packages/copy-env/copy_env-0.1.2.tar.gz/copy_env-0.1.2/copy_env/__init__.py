# -*- coding: utf-8 -*-
"""
Copy requirements from one environment library into another.

Copyright (C) 2021 Dan Eschman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


# %% Imports
import os
import sys
from argparse import ArgumentParser


# %% Variables
_executable_directory = os.path.dirname(sys.executable)


# %% Classes
class MissingDirectoryError(Exception):
    """Raised when neither source or destination directory is defined."""

    # %%% Functions
    def __init__(self,
                 message: str =
                 "Either source or destination directory must be defined."
                 ) -> None:
        self.message = message
        super().__init__(self.message)


# %% Functions
# %%% Private
def _main() -> None:
    # Set up parser
    del sys.argv[0]
    parser = ArgumentParser('copy_environment')
    parser.add_argument("--source",
                        "-s",
                        nargs=1,
                        type=str,
                        help="source python.exe directory")
    parser.add_argument("--destination",
                        "-d",
                        nargs=1,
                        type=str,
                        help="destination python.exe directory")
    parser.set_defaults(func=copy_env)
    # Parse args
    args = parser.parse_args(sys.argv)
    # Run function
    args.func(args)


# %%% Public
def copy_env(source: str = _executable_directory,
             destination: str = _executable_directory) -> None:
    """
    Copy all files from source directory to destination directory.

    Parameters
    ----------
    source : str, default is the directory of this python executable
        Directory of source python executable. Either source or destination
        must be supplied.
    destination : str, default is the directory of this python executable
        Directory of destination python executable. Either source or
        destination must be supplied.
    """
    if source == destination:
        raise MissingDirectoryError

    os.system("cd " + source)
    os.system("python -m pip freeze > _requirements.txt")
    os.system("cd " + destination)
    os.system("python -m pip install -r " + os.path.join(
        source, '_requirements.txt'))


# %% Script
if __name__ == '__main__':
    _main()
