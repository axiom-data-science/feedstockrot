from github.Repository import Repository
from typing import List, Iterable
from .package_sources.condaforge import Condaforge
from .package import Package


class FeedstockRot:
    def __init__(self, packages: Iterable[str]=None):
        self.packages = set()  # type: Iterable[Package]

        if packages is not None:
            self.add(packages)

    def add(self, packages: Iterable[str]):
        self.packages |= set(map(lambda v: Package(v), packages))

    def _add_repositories(self, repositories: Iterable[Repository]):
        self.add(Condaforge.extract_feedstock_names(repositories))

    def add_repositories(self, repositories: Iterable[Repository]):
        repositories = Condaforge.filter_feedstocks(repositories)
        repositories = Condaforge.filter_owner(repositories)
        self._add_repositories(repositories)
