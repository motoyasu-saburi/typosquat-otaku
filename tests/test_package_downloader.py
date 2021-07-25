from typing import Final
from unittest import TestCase

from libraries_io_client import LibrariesIoSearchResult
from package_downloader import PackageDownloader

import httpretty

class TestPackageDownloader(TestCase):

    # TODO download binary(tgz) test
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_download_library(self):
        PACKAGE_URL: Final[str] = "http://localhost:11115/package/example-0.0.1.tgz"

        httpretty.register_uri(
            httpretty.GET,
            PACKAGE_URL,
            # TODO return tgz file from local.
            body='{"origin": "127.0.0.1"}'
        )

        # httpretty.latest_requests().should.have.length_of(1)
        # httpretty.last_request().should.equal(httpretty.latest_requests()[0])
        # httpretty.last_request().body.should.equal('{"origin": "127.0.0.1"}')

        pd = PackageDownloader()
        expect = pd.download_library(
            LibrariesIoSearchResult(
                description="description",
                forks=100,
                stars=200,
                language="PHP",
                platform="",  # TODO
                latest_release_published_at="2021-05-24 14:25:05 UTC",
                latest_stable_release_number="0.0.1",
                license_normalized=False,
                latest_stable_release_published_at="2021-05-24 14:25:05 UTC",
                licenses="MIT",
                name="example",
                package_manager_url="http://localhost:11115/package/example",
                latest_download_url=PACKAGE_URL,
                repository_url="https://localhost:11115/package/example"
            )
        )


