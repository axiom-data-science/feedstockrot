from github.Repository import Repository
from typing import List
from .condaforge import Condaforge
from .package import Package


class FeedstockRot:
    def __init__(self, packages: List[str]):
        self.packages = set(map(lambda v: Package(v), packages))


class GithubFeedstockRot(FeedstockRot):
    def __init__(self, repositories: List[Repository]):
        self._repositories = Condaforge.filter_feedstocks(repositories)
        self._repositories = Condaforge.filter_owner(self._repositories)
        super().__init__(Condaforge.extract_feedstock_names(self._repositories))
