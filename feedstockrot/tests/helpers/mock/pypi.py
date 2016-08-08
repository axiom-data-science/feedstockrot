from responses import RequestsMock
from feedstockrot.package_sources.pypi import Pypi
import re
from .mock import Mock
from .mock import mock_package_list
from ..helpers import escape_regex_format_str


class PypiMock(Mock):

    def setup(self, rsps: RequestsMock):
        for package_name in self.package_names:
            response = {"releases": {
                package['version']: {}
                for package in mock_package_list
                if package['name'] == package_name
            }}
            rsps.add(rsps.GET, Pypi.DEFAULT_PACKAGE_URL.format(package_name), json=response)

        re_notfound = re.compile(escape_regex_format_str(Pypi.DEFAULT_PACKAGE_URL).format("([a-zA-Z-_]+)"))
        for _ in range(self._expected_missing):
            rsps.add(rsps.GET, re_notfound, status=404)
