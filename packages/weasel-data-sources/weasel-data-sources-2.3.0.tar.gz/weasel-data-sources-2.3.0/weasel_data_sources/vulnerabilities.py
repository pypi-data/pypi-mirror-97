""" Fetches information on known vulnerabilities of given software releases """

from datetime import datetime

import requests


class VulnerabilityFetcher:
    """
    Base class of all vulnerability fetchers.
    """

    def get_technology_vulnerabilities(self) -> list:
        """
        Return a list of all vulnerabilities of the technology
        """
        raise NotImplementedError

    def get_version_vulnerabilities(self, version_str) -> list:
        """
        Return a list of all vulnerabilities for a given release.

        :param version_str: The version string of the release, i.e. '3.5.1'.
        """
        raise NotImplementedError


class CVESearchVulnFetcher(VulnerabilityFetcher):
    """
    Fetches known vulnerabilities from a CVESearch instance
    """

    def __init__(self, cpe_base, api_base):
        self._cpe_base = cpe_base
        self._api_base = api_base

    def get_technology_vulnerabilities(self) -> list:
        return self._query_cve_list(self._cpe_base)

    def get_version_vulnerabilities(self, version_str) -> list:
        return self._query_cve_list("{}:{}".format(self._cpe_base, version_str))

    def _query_cve_list(self, cve_query):
        resp = requests.get("{}/cvefor/{}".format(self._api_base, cve_query))
        resp.raise_for_status()
        data = resp.json()

        return [
            {
                "cve": vuln["id"],
                "cwe": vuln["cwe"],
                "cvss": vuln["cvss"],
                "summary": vuln["summary"],
                "time_published": datetime.strptime(
                    vuln["Published"], "%Y-%m-%dT%H:%M:%S"
                ),
                "time_modified": datetime.strptime(
                    vuln["Modified"], "%Y-%m-%dT%H:%M:%S"
                ),
            }
            for vuln in data
        ]
