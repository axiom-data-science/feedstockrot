from github.Repository import Repository
from typing import Set, Iterable
from .package import Package


class FeedstockRot:
    def __init__(self, packages: Iterable[str]=None):
        self.packages = set()  # type: Set[Package]

        if packages is not None:
            self.add(packages)

    def add(self, packages: Iterable[str]):
        self.packages |= set(map(lambda v: Package(v), packages))

    def _add_repositories(self, repositories: Iterable[Repository]):
        self.add(map(lambda repo: repo.name, repositories))

    def add_repositories(self, repositories: Iterable[Repository]):
        # TODO: maybe factor out these literals:
        repositories = filter(
            lambda repo:
                repo.owner.name == 'conda-forge' and
                repo.name.endswith('-feedstock'),
            repositories
        )
        self._add_repositories(repositories)
