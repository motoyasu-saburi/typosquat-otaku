import tempfile
from dataclasses import dataclass
from typing import List

import requests as requests

from libraries_io_client import LibrariesIoClient, LibrariesIoSearchResult


@dataclass
class PackageDownloader:

    def download_libraries(self, keyword: str):
        lic = LibrariesIoClient()
        packages: List[LibrariesIoSearchResult] = lic.search_package(keyword)
        for pkg in packages:
            self.download_library(pkg)

    def download_library(self, package: LibrariesIoSearchResult) -> str:
        """
        :param package: download target package
        :return: downloaded file path
        """
        if package.language == "Java":
            pass
            # Case: Binary
            # TODO
            #   - Download .jar
            #   - unzip .jar
            #   - find .class files
            #   - javap -v target.class ( create disassembly file )
            #   - extract comment out ( comment out is original code extracted by the assembler )
            #   - extract URL & high entropy (obfuscation) string
        elif package.language in ["python", "PHP"]:
            pass
            # Memo: In the case of Python & PHP, "LibrariesIO" may not provide a Download Url.
            # The Script language allows for easy string checking.
            # TODO ...
        elif package.language == "go":
            pass
            # Memo: In the case of GO, "LibrariesIO" may not provide a Download Url.
            # TODO ...
        elif package.language == "ruby":
            pass
            # TODO
            #   - download gem file (from url)
            #   - tar xvf {targetfile}.gem -C {unzip target directory}
            #   - unzip "data.tar.gz"
            #   - (The Script language allows for easy string checking.)
        elif package.language in ["npm", "typescript"]:
            splitted_url = package.latest_download_url.split("/")
            try:
                url_data = requests.get(splitted_url).content  # TODO
                with tempfile.NamedTemporaryFile() as tf:
                    tf.write(url_data)
                    print(tf.name)
                    tf.close()
            except Exception as e:
                print(e)

            # TODO
            #   - download library tgz file (from url)
            #   - unzip "target-library.tgz"
            #   - search `.js`, `.ts` files
            #   - (The Script language allows for easy string checking.)
        elif package.language == "c#":
            pass
            # TODO
            #  - download nupkg file
            #  - rename & unzip nupkg
            #  - analyze binary file...?