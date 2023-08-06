# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for reading from list files"""

import os
from typing import List, Optional


def read_list(listpath: str, encoding: Optional[str] = None) -> List[str]:
    """Reads the given list file and returns its contents"""
    with open(listpath, mode="r", encoding=encoding) as list_file:
        return [line.strip() for line in list_file.read().splitlines() if line]


def add_list(listpath: str, entry: str):
    """Appends the given value to the list file"""
    os.makedirs(os.path.dirname(listpath), exist_ok=True)
    with open(listpath, mode="a") as list_file:
        print(entry, file=list_file)


def write_list(path: str, contents: List[str]):
    """Writes a list file containing the given list"""
    with open(path, "w") as file:
        for value in contents:
            print(value, file=file)
