from .mock import Mock
from .mock import mock_package_list
from responses import RequestsMock
from feedstockrot.package_sources.condaforge import Condaforge


class AnacondaMock(Mock):

    def __enter__(self):
        self._old_repodata = Condaforge._repodata
        Condaforge._repodata = None

    def __exit__(self, *exc):
        Condaforge._repodata = self._old_repodata

    def setup(self, rsps: RequestsMock):
        response = {"packages": {
            "{}-{}".format(package['name'], package['version']): package
            for package in mock_package_list
            if package['name'] in self.package_names
        }}
        rsps.add(
            rsps.GET,
            Condaforge._DEFAULT_REPODATA_URL.format(Condaforge._DEFAULT_OWNER, Condaforge._DEFAULT_PLATFORM),
            json=response
        )
