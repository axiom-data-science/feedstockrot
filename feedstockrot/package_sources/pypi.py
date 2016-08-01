from .source import Source
import requests
from json.decoder import JSONDecodeError
from typing import Dict, Set


class Pypi(Source):
    DEFAULT_PACKAGE_URL = "https://pypi.python.org/pypi/{}/json"

    @classmethod
    def _fetch_package(cls, name) -> Dict:
        return requests.get(cls.DEFAULT_PACKAGE_URL.format(name)).json()

    @classmethod
    def _fetch_package_versions(cls, name: str) -> Set[str]:
        try:
            resp = cls._fetch_package(name)
        except JSONDecodeError:
            return None
        return resp['releases'].keys()
