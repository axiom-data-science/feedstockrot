from github.Repository import Repository
from typing import List
from .condaforge import Condaforge
from packaging.version import Version


class FeedstockRot:
    def __init__(self, packages: List[str]):
        self.packages = packages

    def latest_versions(self) -> List[Version]:
        latest_package_versions = {}
        for package in self.packages:
            versions = Condaforge.find_package_versions(package)
            versions = map(lambda v: Version(v), versions)
            latest_package_versions[package] = max(versions)
        return latest_package_versions


class GithubFeedstockRot(FeedstockRot):
    def __init__(self, repositories: List[Repository]):
        self._repositories = Condaforge.filter_feedstocks(repositories)
        self._repositories = Condaforge.filter_owner(self._repositories)
        super().__init__(Condaforge.extract_feedstock_names(self._repositories))
