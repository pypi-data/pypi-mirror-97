""" Helper tools which are used by other modules """
import hashlib
from distutils.version import LooseVersion

import ssdeep


def _hexdigest(hash_object):
    if hasattr(hash_object, "hexdigest"):
        return hash_object.hexdigest()

    return hash_object.digest()


def get_hashes(path, blocksize=4096, hash_types=None):
    """
    Calculates the MD5, SHA1, SHA256 and SHA512 hashes of a given file

    :param path:
    :param blocksize:
    :return:
    """
    hashes = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "sha512": hashlib.sha512(),
        "ssdeep": ssdeep.Hash(),
    }

    if hash_types is None:
        hash_types = {"sha512"}

    with open(path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(blocksize), b""):
            for algo in hash_types:
                hashes[algo].update(chunk)

    return {hash_type: _hexdigest(hashes[hash_type]) for hash_type in hash_types}


class VeryLooseVersion(LooseVersion):
    """
    Handles comparisons between versions with mixed strings and integers
    """

    def _cmp(self, other, only_branch=False):  # pylint: disable=W0221
        if isinstance(other, str):
            other = VeryLooseVersion(other)

        if only_branch:
            if len(self.version) == len(other.version):
                cmp_to = max(len(self.version) - 1, 2)
            else:
                cmp_to = min(len(self.version), len(other.version))
            ver1 = self.version[:cmp_to]
            ver2 = other.version[:cmp_to]
        else:
            ver1 = self.version
            ver2 = other.version

        for comp1, comp2 in zip(ver1, ver2):
            try:
                if comp1 < comp2:
                    return -1
                if comp1 > comp2:
                    return 1
            except TypeError:
                return -1

        # Still here -> Versions have different number of elements or are identical
        if len(ver1) == len(ver2):
            return 0
        if len(ver1) < len(ver2):
            return -1
        return 1

    def same_branch(self, other):
        """
        Evaluates whether two versions are of the same branch

        :param other: Another `VeryLooseVersion` instance
        """
        return self._cmp(other, only_branch=True) == 0
