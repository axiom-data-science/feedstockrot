from responses import RequestsMock
from feedstockrot.package_sources.github import Github
import re
from .mock import Mock
from .mock import mock_package_list
from ..helpers import escape_regex_format_str


class GithubMock(Mock):

    def setup(self, rsps: RequestsMock):
        for package_name in self.package_names:
            response = [
                {"ref": "refs/tags/{}".format(package['version'])}
                for package in mock_package_list
                if package['name'] == package_name
            ]

            github_name = package_name
            if '/' not in github_name:
                github_name = package_name + "/" + package_name

            rsps.add(rsps.GET, Github._REFS_URL.format(github_name), json=response)

        re_notfound = re.compile(escape_regex_format_str(Github._REFS_URL).format("([a-zA-Z-_.]+)"))
        for _ in range(self._expected_missing):
            rsps.add(rsps.GET, re_notfound, status=404)
