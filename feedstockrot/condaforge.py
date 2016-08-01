from github.Repository import Repository
from typing import List, Set
import requests
from packaging.version import Version


class Condaforge:

    DEFAULT_OWNER = 'conda-forge'
    DEFAULT_PLATFORM = 'linux-64'

    _repodata = None

    @classmethod
    def extract_feedstock_names(cls, repos: List[Repository]) -> List[str]:
        return map(lambda repo: repo.name.replace('-feedstock', ''), repos)

    @classmethod
    def filter_feedstocks(cls, repos: List[Repository]) -> List[Repository]:
        """
        Filter a list of repositories down to only the ones that are valid feedstocks
        """
        return [repo for repo in repos if repo.name.endswith('-feedstock')]

    @classmethod
    def filter_owner(cls, repos: List[Repository], owner=DEFAULT_OWNER):
        """
        Filter a list of repositories to only those owned by the specified user.
        This is meant to be used to hide forks and only show official repositories.
        """
        return [repo for repo in repos if repo.owner.name == owner]

    @classmethod
    def _get_repodata(cls):
        """
        {
            "packages": {
                "$package_name": {
                    "name": "",
                    "version": "",
                    ...
                }
            }
        }
        """
        if cls._repodata is None:
            url = 'https://conda.anaconda.org/{}/{}/repodata.json'.format(cls.DEFAULT_OWNER, cls.DEFAULT_PLATFORM)
            cls._repodata = requests.get(url).json()
        return cls._repodata

    # don't expose repodata directly so that in the future we can
    # transition to a search API, as conda's repodata method probably won't scale

    @classmethod
    def _find_package_versions(cls, name: str) -> Set[Version]:
        versions = set()
        for package_name, package in cls._get_repodata()['packages'].items():
            if package['name'] == name:
                versions.add(package['version'])
        return versions

    @classmethod
    def get_package_versions(cls, name: str) -> Set[Version]:
        return map(lambda v: Version(v), cls._find_package_versions(name))
