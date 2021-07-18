import os
from dataclasses import dataclass
from typing import List, Optional

from pip._vendor import requests

import logging

@dataclass
class LibrariesIoSearchResult:
    description: str
    forks: int
    stars: int
    language: str
    platform: str
    latest_release_published_at: str  # Datetime, "2021-05-24 14:25:05 UTC",
    latest_stable_release_number: str  # "1.4.1
    license_normalized: bool
    latest_stable_release_published_at: str  # Datetime, "2021-05-24 14:25:05 UTC",
    licenses: Optional[str]  # MIT
    name: str  # grunt
    package_manager_url: str  # "https://www.npmjs.com/package/grunt"
    latest_download_url: str  # "https://registry.npmjs.org/grunt/-/grunt-1.4.1.tgz",
    repository_url: str  # "https://github.com/gruntjs/grunt"


def _mapping_libraries_io_search_result(json: any) -> List[LibrariesIoSearchResult]:
    return list(map(lambda j: LibrariesIoSearchResult(
        description=j['description'],
        forks=j['forks'],
        stars=j['stars'],
        language=j['language'],
        platform=j['platform'],
        latest_release_published_at=j['latest_release_published_at'],
        latest_stable_release_number=j['latest_stable_release_number'],
        latest_stable_release_published_at=j['latest_stable_release_published_at'],
        licenses=j['licenses'],
        license_normalized=j['license_normalized'],
        name=j['name'],
        package_manager_url=j['package_manager_url'],
        latest_download_url=j['latest_download_url'],
        repository_url=j['repository_url']
    ), json))


@dataclass
class LibrariesIoClient:
    API_KEY = os.getenv("LIBRARIES_IO_API_KEY")

    def search_package(self, keyword: str) -> List[LibrariesIoSearchResult]:
        SEARCH_API_URL = f"https://libraries.io/api/search?q=${keyword}&api_key=${self.API_KEY}"
        try:
            res = requests.get(SEARCH_API_URL)
            return _mapping_libraries_io_search_result(res.json())
        except Exception as e:
            logging.error(e)
