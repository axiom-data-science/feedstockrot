from .source import Source
from github.Repository import Repository
from typing import Set, Iterable, Dict
import requests
import yaml


class Condaforge(Source):

    DEFAULT_OWNER = 'conda-forge'
    DEFAULT_PLATFORM = 'linux-64'
    DEFAULT_REPODATA_URL = 'https://conda.anaconda.org/{}/{}/repodata.json'
    DEFAULT_RECIPE_URL = 'https://raw.githubusercontent.com/conda-forge/{}-feedstock/master/recipe/meta.yaml'

    _repodata = None

    @classmethod
    def extract_feedstock_names(cls, repos: Iterable[Repository]) -> Iterable[str]:
        return map(lambda repo: repo.name.replace('-feedstock', ''), repos)

    @classmethod
    def filter_feedstocks(cls, repos: Iterable[Repository]) -> Iterable[Repository]:
        """
        Filter a list of repositories down to only the ones that are valid feedstocks
        """
        return filter(lambda repo: repo.name.endswith('-feedstock'), repos)

    @classmethod
    def filter_owner(cls, repos: Iterable[Repository], owner=DEFAULT_OWNER) -> Iterable[Repository]:
        """
        Filter a list of repositories to only those owned by the specified user.
        This is meant to be used to hide forks and only show official repositories.
        """
        return filter(lambda repo: repo.owner.name == owner, repos)

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
            url = cls.DEFAULT_REPODATA_URL.format(cls.DEFAULT_OWNER, cls.DEFAULT_PLATFORM)
            cls._repodata = requests.get(url).json()
        return cls._repodata

    @classmethod
    def _fetch_package_versions(cls, name: str) -> Set[str]:
        versions = set()
        for package_name, package in cls._get_repodata()['packages'].items():
            if package['name'] == name:
                versions.add(package['version'])
        return versions

    @classmethod
    def _get_recipe(cls, name: str) -> Dict:
        resp = requests.get(cls.DEFAULT_RECIPE_URL.format(name))
        if resp.status_code != 200:
            return None
        return yaml.load(resp.text)

    @classmethod
    def get_recipe_urls(cls, name: str) -> Iterable[str]:
        """
        Get URLs for a feedstock that may be useful for discerning project info/versions from other sources
        """
        recipe = cls._get_recipe(name)
        urls = []

        if recipe is None:
            return urls

        if 'about' in recipe and 'home' in recipe['about']:
            urls.append(recipe['about']['home'])
        if 'source' in recipe and 'url' in recipe['source']:
            urls.append(recipe['source']['url'])

        return urls
