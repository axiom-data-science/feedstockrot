from .source import Source
from typing import Set, List, Dict
import requests
import yaml


class Condaforge(Source):

    _DEFAULT_OWNER = 'conda-forge'
    _DEFAULT_PLATFORMS = ['linux-64', 'osx-64', 'win-64']
    _DEFAULT_REPODATA_URL = 'https://conda.anaconda.org/{}/{}/repodata.json'
    _DEFAULT_RECIPE_URL = 'https://raw.githubusercontent.com/conda-forge/{}-feedstock/master/recipe/meta.yaml'

    _repodata = {}

    @classmethod
    def _possible_names(cls, name: str):
        names = [name]
        if name.endswith('-feedstock'):
            names.append(name[:-len('-feedstock')])
        return names

    @classmethod
    def _get_repodata(cls, platform) -> Dict:
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
        if platform not in cls._repodata:
            url = cls._DEFAULT_REPODATA_URL.format(cls._DEFAULT_OWNER, platform)
            response = requests.get(url)
            if response.status_code != 200:
                return None

            cls._repodata[platform] = response.json()
        return cls._repodata[platform]

    @classmethod
    def _get_repodata_packages_aggregate(cls) -> List[Dict]:
        packages = []
        for platform in cls._DEFAULT_PLATFORMS:
            repodata = cls._get_repodata(platform)
            if repodata is None:
                continue

            platform_packages = repodata['packages'].values()
            packages += platform_packages
        return packages

    @classmethod
    def _fetch_versions(cls, name: str) -> Set[str]:
        versions = set()
        for package in cls._get_repodata_packages_aggregate():
            if package['name'] == name:
                versions.add(package['version'])
        return versions if len(versions) > 0 else None

    def _get_recipe(self) -> Dict:
        resp = requests.get(self._DEFAULT_RECIPE_URL.format(self.name))
        if resp.status_code != 200:
            return None
        return yaml.load(resp.text)

    def get_recipe_urls(self) -> List[str]:
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
