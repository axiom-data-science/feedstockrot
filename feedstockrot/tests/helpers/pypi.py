from contextlib import contextmanager
from responses import RequestsMock
from .condaforge import mock_repodata
from feedstockrot.package_sources.pypi import Pypi


@contextmanager
def mock_pypi(package_name):
    with RequestsMock() as rsps:
        response_json = {"releases": {
            package['version']: {}
            for package_key, package in mock_repodata['packages'].items()
            if package['name'] == package_name
        }}
        rsps.add(rsps.GET, Pypi.DEFAULT_PACKAGE_URL.format(package_name), json=response_json)

        yield
        # to make sure gc doesn't collect:
        assert rsps
