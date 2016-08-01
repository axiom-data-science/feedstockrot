from .source import Source
import requests
from typing import Dict, Set


class Pypi(Source):
    DEFAULT_PACKAGE_URL = "https://pypi.python.org/pypi/{}/json"

    @classmethod
    def _fetch_package(cls, name) -> Dict:
        resp = requests.get(cls.DEFAULT_PACKAGE_URL.format(name))
        if resp.status_code != 200:
            return None
        return resp.json()

    @classmethod
    def _fetch_package_versions(cls, name: str) -> Set[str]:
        resp = cls._fetch_package(name)
        if not resp:
            return None
        return resp['releases'].keys()
