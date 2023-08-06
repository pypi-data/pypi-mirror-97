# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for creating and parsing Manifest files"""

import csv
import os
from enum import Enum
from io import StringIO
from typing import Dict, Iterable, Optional

from portmod.fs.util import get_hash
from portmod.source import HashAlg


class ManifestMissing(Exception):
    """Inidcates a missing or invalid manifest entry"""


def _grouper(n: int, iterable):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip(*args)


class FileType(Enum):
    """Type of a ManifestEntry"""

    DIST = "DIST"
    MISC = "MISC"


class ManifestEntry:
    def __init__(
        self, name: str, filetype: FileType, size: int, hashes: Dict[HashAlg, str]
    ):
        self.name = name
        if not isinstance(filetype, FileType):
            raise Exception(
                "filetype {} of manifest entry must be a FileType".format(filetype)
            )
        self.file_type = filetype
        self.hashes = hashes
        self.size = int(size)

    def __str__(self):
        io = StringIO()
        writer = csv.writer(io, delimiter=" ")
        writer.writerow(
            [
                self.file_type.name,
                self.name,
                self.size,
            ]
            + [
                item
                for elems in [[h.value, self.hashes[h]] for h in sorted(self.hashes)]
                for item in elems
            ]
        )
        return io.getvalue().strip()

    @classmethod
    def from_path(
        cls,
        filetype: FileType,
        path: str,
        relative_path: str,
        algs: Iterable[HashAlg] = (HashAlg.BLAKE3,),
    ) -> "ManifestEntry":
        hashes = dict(zip(algs, get_hash(path, tuple(algs))))
        size = os.path.getsize(path)

        return ManifestEntry(relative_path, filetype, size, hashes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ManifestEntry):
            return False

        if self.size != other.size:
            return False

        # If no hashes are the same type, we cannot meaningfully compare
        # the two manifest entries
        if not any(alg in other.hashes for alg in self.hashes):
            return False
        return all(
            other.hashes.get(alg) == value
            for alg, value in self.hashes.items()
            if alg in other.hashes
        )


class Manifest:
    def __init__(self, file: Optional[str] = None):
        self.entries = {}
        self.file = file
        if file is not None and os.path.exists(file):
            with open(file, "r") as manifest:
                self.entries = Manifest.from_reader(manifest)

    @classmethod
    def from_reader(cls, reader: Iterable[str]) -> Dict[str, ManifestEntry]:
        csvdata = csv.reader(reader, delimiter=" ")
        entries = {}
        for line in csvdata:
            filetype = line[0]
            name = line[1]
            size = int(line[2])
            hashes = {}
            for alg, value in _grouper(2, line[3:]):
                if alg in HashAlg:
                    hashes[HashAlg[alg]] = value
            entries[name] = ManifestEntry(name, FileType[filetype], size, hashes)
        return entries

    def add_entry(self, entry: ManifestEntry):
        if entry is None:
            raise Exception("Adding None to manifest")
        ours = self.entries.get(entry.name)
        if ours is None or str(ours) != str(entry):
            self.entries[entry.name] = entry

    def write(self, file: Optional[str] = None):
        if file is not None:
            self.file = file
        if self.file is not None:
            with open(self.file, "w") as manifest:
                lines = [str(entry) for entry in self.entries.values()]
                lines.sort()
                for line in lines:
                    print(line, file=manifest)

    def get(self, name: str) -> Optional[ManifestEntry]:
        return self.entries.get(name)

    def __eq__(self, other: object) -> bool:
        # Check that all corresponding hashes match.
        if not isinstance(other, Manifest):
            return False

        for name, manifest in self.entries.items():
            if not other.get(name):
                return False
            if manifest != other.get(name):
                return False

        for name, manifest in other.entries.items():
            if name not in self.entries:
                return False

        return True

    def to_json(self):
        return [str(entry) for entry in self.entries.values()]

    @classmethod
    def from_json(cls, data):
        if data:
            manifest = Manifest()
            manifest.entries = Manifest.from_reader(data)
            return manifest
        return None
