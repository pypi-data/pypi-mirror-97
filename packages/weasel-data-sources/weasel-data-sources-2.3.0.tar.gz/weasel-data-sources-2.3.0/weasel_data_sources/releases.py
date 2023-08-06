""" Fetches release information and files from different data sources. """

import base64
import io
import os
import re
import subprocess  # nosec
import xml.etree.ElementTree as ET  # nosec
from contextlib import contextmanager
from datetime import datetime

import pytz
import requests
import svn.local
import svn.remote
from git import Repo

from weasel_data_sources.utils import VeryLooseVersion, get_hashes


class ReleaseFetcher:
    """
    Base class of all release info fetchers.
    """

    @staticmethod
    def _sort_release_metadata(metadata: list) -> list:
        return sorted(metadata, key=lambda x: VeryLooseVersion(x["version_str"]))

    def get_release_metadata(self) -> list:
        """
        Return a list of all releases known by the datasource

        :return:
        """
        raise NotImplementedError

    def get_file_list(self, version_str) -> dict:
        """
        Return a dict of files, including their size and optionally hashes for identification

        :param version_str: The version string of the release, i.e. '3.5.1'.
        :return:
        """
        raise NotImplementedError

    def retrieve_file(self, version_str, filename):
        """
        Stores a specified file in the given target location.

        :param version_str: The version string of the release, i.e. '3.5.1'.
        :param filename: The filename and path within the data source, i.e. 'foo/bar.txt'
        :return:
        """
        raise NotImplementedError


class CDNJSFetcher(ReleaseFetcher):
    """
    Fetcher to retrieve data from cdnjs.com
    """

    _re_sri = re.compile(r"(?P<algorithm>[^-]+)-(?P<b64hash>[\w+/]+==)")

    def __init__(self, library_name):
        """
        :param library_name: The name of the library on `cdnjs.com`
        """
        self._library_name = library_name

        resp = requests.get("https://api.cdnjs.com/libraries/{}".format(library_name))
        resp.raise_for_status()
        data = resp.json()

        self._latest = data["version"]
        self._releases = {}
        for asset in data["assets"]:
            self._releases[asset["version"]] = {
                f: self._decode_hash(h) for f, h in asset["sri"].items()
            }

    def _decode_hash(self, sri):
        match = self._re_sri.fullmatch(sri)
        if match.group("algorithm") != "sha512":
            raise ValueError("Unsupported algorithm: " + match.group("algorithm"))

        return base64.standard_b64decode(match.group("b64hash")).hex()

    def get_release_metadata(self):
        return self._sort_release_metadata(
            [
                {"version_str": ver, "latest": self._latest == ver, "published": True}
                for ver in self._releases
            ]
        )

    def get_file_list(self, version_str):
        return {
            file_name: {"hashes": {"sha512": hash_sum}}
            for file_name, hash_sum in self._releases[version_str].items()
        }

    @contextmanager
    def retrieve_file(self, version_str, filename):
        resp = requests.get(
            "https://cdnjs.cloudflare.com/ajax/libs/{}/{}/{}".format(
                self._library_name, version_str, filename
            ),
        )

        resp.raise_for_status()
        with io.BytesIO(resp.content) as file_object:
            yield file_object


class RepositoryFetcher(ReleaseFetcher):
    """
    Base fetcher and main logic to retrieve data from Git and SVN repositories
    """

    def __init__(self, repo_url, local_path, tag_regex=None, tag_substitute=None):
        self._repo_url = repo_url
        self._local_path = local_path

        if not os.path.isdir(local_path):
            self._clone_repository()
        self._update_and_prepare_repository()

        self._tag_dates = {}
        self._tag_mapping = {}
        self._version_pattern = (
            re.compile(tag_regex, flags=re.IGNORECASE)
            if tag_regex
            else re.compile(r"^v?((?:\d+\.\d+).*)$", re.IGNORECASE)
        )

        # Create a mapping from parsed version strings to tag names
        for tag in self._get_tags():
            ver = self._version_pattern.search(tag)
            if ver is None:
                print("\tSkipped Tag", tag)
                continue

            version_str = ver.group(1)
            if tag_substitute:
                version_str = re.sub(tag_substitute[0], tag_substitute[1], version_str)

            self._tag_mapping[version_str] = tag

    def _clone_repository(self):
        raise NotImplementedError

    def _update_and_prepare_repository(self):
        raise NotImplementedError

    def _get_tags(self):
        raise NotImplementedError

    def _checkout_release(self, version_str) -> str:
        raise NotImplementedError

    def get_release_metadata(self) -> list:
        return self._sort_release_metadata(
            [
                {
                    "version_str": ver,
                    "publication_date": self._tag_dates[tag].astimezone(pytz.UTC),
                }
                for ver, tag in self._tag_mapping.items()
            ]
        )

    def get_file_list(self, version_str) -> dict:
        release_path = self._checkout_release(version_str)

        file_list = {}
        for root, dirs, files in os.walk(release_path, topdown=True):
            # Inplace modification will skip excluded directories when iterating over files
            dirs[:] = [d for d in dirs if d not in {".git"}]

            for file_name in files:
                full_file_path = os.path.join(root, file_name)

                if os.path.islink(full_file_path):
                    continue

                repo_file_name = os.path.relpath(full_file_path, release_path)
                file_list[repo_file_name] = {"hashes": get_hashes(full_file_path)}

        return file_list

    @contextmanager
    def retrieve_file(self, version_str, filename):
        release_path = self._checkout_release(version_str)
        source_path = os.path.join(release_path, filename)

        with open(source_path, "rb") as source_fp:
            yield source_fp


class GitFetcher(RepositoryFetcher):
    """
    Fetcher to retrieve data from arbitrary Git repositories
    """

    def __init__(self, repo_url, local_path, tag_regex=None, tag_substitute=None):
        """
        :param repo_url: Path to the Git repository,\
         i.e. `https://gitlab.com/weasel-project/weasel-data-sources.git`
        :param local_path: Path to a local copy of the repo. Will be created if it does not exist.
        :param tag_regex: Regex capturing versions from tags. Default: r"`^v?((?:\\d+\\.\\d+).*)$`"
        :param tag_substitute: Tuple of a regex matching parts of the captured version string\
         and a string to replace it with
        """
        self._repo = None
        self._current_checkout = None
        super().__init__(repo_url, local_path, tag_regex, tag_substitute)

    def _clone_repository(self):
        Repo.clone_from(self._repo_url, self._local_path)

    def _update_and_prepare_repository(self):
        self._repo = Repo(self._local_path)

        # Checkout an arbitrary branch to ensure the following fetch will work
        branch = self._repo.branches[0]
        self._repo.git.checkout(branch)
        self._current_checkout = branch

        self._repo.remotes.origin.pull()

    def _get_tags(self):
        tags = set()
        for tag in self._repo.tags:
            tags.add(tag.name)
            self._tag_dates[tag.name] = tag.commit.committed_datetime

        return tags

    def _checkout_release(self, version_str) -> str:
        tag = self._tag_mapping[version_str]
        if tag != self._current_checkout:
            self._repo.git.checkout(tag)
            self._current_checkout = tag

        return self._local_path


class SVNFetcher(RepositoryFetcher):
    """
    Fetcher to retrieve data from arbitrary SVN repositories
    """

    def __init__(self, repo_url, local_path, tag_regex=None, tag_substitute=None):
        """
        :param repo_url: Path to the SVN repository,\
         i.e. `https://core.svn.wordpress.org/`
        :param local_path: Path to a local copy of the repo. Will be created if it does not exist.
        :param tag_regex: Regex capturing versions from tags. Default: r"`^v?((?:\\d+\\.\\d+).*)$`"
        :param tag_substitute: Tuple of a regex matching parts of the captured version string\
         and a string to replace it with
        """
        self._repo = None
        super().__init__(repo_url, local_path, tag_regex, tag_substitute)

    def _clone_repository(self):
        print("Clone repository")
        repo = svn.remote.RemoteClient(self._repo_url)
        repo.checkout(self._local_path)

    def _update_and_prepare_repository(self):
        print("Update repository")
        self._repo = svn.local.LocalClient(self._local_path)
        self._repo.update()

    def _get_tags(self):
        print("Get Tags")
        svn_output = subprocess.getoutput(
            "svn ls --xml {}".format(os.path.join(self._local_path, "tags"))
        )
        tree = ET.fromstring(svn_output)  # nosec
        tags = []

        for directory in tree.find("list"):
            tag = directory.find("name").text
            timestamp = directory.find("./commit/date").text
            self._tag_dates[tag] = datetime.strptime(
                timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=pytz.UTC)
            tags.append(tag)

        return tags

    def _checkout_release(self, version_str):
        return os.path.join(self._local_path, "tags", self._tag_mapping[version_str])
