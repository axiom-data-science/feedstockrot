from .source import Source
from typing import Set, Iterable, Dict
import requests
import yaml


class Condaforge(Source):

    _DEFAULT_OWNER = 'conda-forge'
    _DEFAULT_PLATFORM = 'linux-64'
    _DEFAULT_REPODATA_URL = 'https://conda.anaconda.org/{}/{}/repodata.json'
    _DEFAULT_RECIPE_URL = 'https://raw.githubusercontent.com/conda-forge/{}-feedstock/master/recipe/meta.yaml'

    _repodata = None

    @classmethod
    def _possible_names(cls, name: str):
        names = [name]
        if name.endswith('-feedstock'):
            names.append(name[:-len('-feedstock')])
        return names

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
            url = cls._DEFAULT_REPODATA_URL.format(cls._DEFAULT_OWNER, cls._DEFAULT_PLATFORM)
            cls._repodata = requests.get(url).json()
        return cls._repodata

    @classmethod
    def _fetch_versions(cls, name: str) -> Set[str]:
        versions = set()
        for package_name, package in cls._get_repodata()['packages'].items():
            if package['name'] == name:
                versions.add(package['version'])
        return versions

    def _get_recipe(self) -> Dict:
        resp = requests.get(self._DEFAULT_RECIPE_URL.format(self.name))
        if resp.status_code != 200:
            return None
        return yaml.load(resp.text)

    def get_recipe_urls(self) -> Iterable[str]:
        """
        Get URLs for a feedstock that may be useful for discerning project info/versions from other sources
        """
        recipe = self._get_recipe()
        urls = []

        if recipe is None:
            return urls

        if 'about' in recipe and 'home' in recipe['about']:
            urls.append(recipe['about']['home'])
        if 'source' in recipe and 'url' in recipe['source']:
            urls.append(recipe['source']['url'])

        return urls
