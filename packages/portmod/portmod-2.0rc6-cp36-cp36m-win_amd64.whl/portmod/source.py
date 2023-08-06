# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import enum
import os
from typing import Any, Dict

from portmod.globals import env
from portmod.l10n import l10n


def get_archive_basename(archive: str) -> str:
    """Returns archive name minus extension(s)"""
    basename, _ = os.path.splitext(archive)
    # Hacky way to handle tar.etc having multiple extensions
    if basename.endswith("tar"):
        basename, _ = os.path.splitext(basename)
    return basename


class EnumMeta(enum.EnumMeta):
    def __contains__(cls, item: Any):
        return item in {member.value for member in cls.__members__.values()}  # type: ignore


class HashAlg(enum.Enum, metaclass=EnumMeta):
    """
    Class for interacting with supported hash algorithms that can be used in manifests
    """

    BLAKE2B = "BLAKE2B"
    MD5 = "MD5"
    SHA512 = "SHA512"
    BLAKE3 = "BLAKE3"

    def __lt__(self, other):
        return self.value < other.value


class LocalHashError(Exception):
    """Exception indicating an unexpected download file"""


class Source:
    """
    Class used for storing information about download files without manifest information
    """

    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.path = os.path.join(env.DOWNLOAD_DIR, name)
        self.basename = get_archive_basename(name)

    def __repr__(self):
        return self.url

    def to_json(self):
        return {"url": self.url, "name": self.name}

    def __eq__(self, other):
        if not isinstance(other, Source):
            return False
        return self.url == other.url and self.name == other.name

    def __hash__(self):
        return hash((self.url, self.name))


class SourceManifest(Source):
    """Class used for storing information about download files"""

    def __init__(self, source: Source, hashes: Dict[HashAlg, str], size: int):
        super().__init__(source.url, source.name)
        self.hashes = hashes
        self.size = size

    def __hash__(self):
        return hash((self.url, self.name, tuple(self.hashes)))

    def as_source(self):
        return Source(self.url, self.name)

    def check_file(self, filename: str, raise_ex=False) -> bool:
        """
        Returns true if and only if the hash of the given file
        matches the stored hash
        """
        from portmod.fs.util import get_hash

        hashes_to_check = sorted(self.hashes)
        if len(hashes_to_check) > 1 and HashAlg.MD5 in hashes_to_check:
            # Ignore MD5 unless it's the only hash. It's neither particularly fast, nor reliable
            # It's only used since certain services will supply an MD5 hash which we can compare to
            hashes_to_check.remove(HashAlg.MD5)
        results = get_hash(filename, tuple(sorted(self.hashes)))
        for halg, result in zip(sorted(self.hashes), results):
            if self.hashes[halg] != result:
                if raise_ex:
                    raise LocalHashError(
                        l10n(
                            "local-hash-mismatch",
                            filename=filename,
                            hash=halg.name,
                            hash1=self.hashes[halg],
                            hash2=result,
                        )
                    )
                return False
        return True
