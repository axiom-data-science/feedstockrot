from .source import Source, PackageInfo
import requests
from typing import Dict, Set, List
import logging
from urllib.parse import urlparse
from pathlib import PurePosixPath
from os.path import splitext

class Github(Source):

    # For a Github object the `name` is owner/repo as a single string
    # so the URLs below are formatted with that assumption

    _INFO_URL = 'https://api.github.com/repos/{}'
    _RELEASES_URL = 'https://api.github.com/repos/{}/releases'
    _REFS_URL = 'https://api.github.com/repos/{}/git/refs'
    _TAGS_URL = 'https://api.github.com/repos/{}/git/refs/tags'
    _TAG_PREFIX = 'refs/tags/'

    @classmethod
    def _possible_names(cls, package: PackageInfo) -> List[str]:
        names = list()
        for url_str in package.get_urls():
            url = urlparse(url_str)
            host = url.netloc
            if not host.endswith('github.com'):
                continue

            path = PurePosixPath(url.path)
            parts = path.parts
            if path.is_absolute():
                parts = parts[1:]

            if len(parts) >= 2:
                # Get the first 2 path components without extensions
                # this should handle:
                # - owner/project
                # - owner/project.git
                # - owner/project/releases

                name = PurePosixPath(parts[0])
                # strip off .git if the project name contains it
                # don't just strip off any ext because "." is valid
                name_project = parts[1]
                if name_project.endswith('.git'):
                    name_project = name_project[:-len('.git')]
                name = name.joinpath(name_project)

                names.append(str(name))

        return names

    @classmethod
    def _fetch_tags(cls, name: str) -> Dict:
        response = requests.get(cls._TAGS_URL.format(name))
        if response.status_code != 200:
            return None
        tags_data = response.json()

        versions = set()
        for tag_data in tags_data:
            ref = tag_data['ref']
            if ref.startswith(cls._TAG_PREFIX):
                tag = ref[len(cls._TAG_PREFIX):]
                versions.add(tag)
        return versions

    @classmethod
    def _fetch_versions(cls, name: str) -> Set[str]:
        return cls._fetch_tags(name)
