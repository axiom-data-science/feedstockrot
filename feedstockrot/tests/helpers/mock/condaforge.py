from .mock import Mock
from .mock import mock_package_list
from responses import RequestsMock
from feedstockrot.package_sources.condaforge import Condaforge
import yaml


class CondaforgeRepoMock(Mock):

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


class CondaforgeRecipeMock(Mock):

    def setup(self, rsps: RequestsMock):
        for package_name in self.package_names:
            package = [package for package in mock_package_list if package['name'] == package_name][-1]
            recipe = {"package": {"name": package_name, "version": package['version']}}
            if "source_url" in package:
                recipe["source"] = {"url": package['source_url']}
            if "home_url" in package:
                recipe['about'] = {"home": package['home_url']}
            response = yaml.dump(recipe)
            rsps.add(rsps.GET, Condaforge._DEFAULT_RECIPE_URL.format(package_name), body=response)
