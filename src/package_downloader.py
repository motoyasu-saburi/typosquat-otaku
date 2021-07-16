from dataclasses import dataclass
from typing import List

from libraries_io_client import LibrariesIoClient, LibrariesIoSearchResult


@dataclass
class PackageDownloader:

    def download_library(self, keyword: str) -> None:
        lic = LibrariesIoClient()
        packages: List[LibrariesIoSearchResult] = lic.search_package(keyword)
        for pkg in packages:
            if pkg.language == "Java":
                pass
                # Case: Binary
                # TODO
                #   - Download .jar
                #   - unzip .jar
                #   - find .class files
                #   - javap -v target.class ( create disassembly file )
                #   - extract comment out ( comment out is original code extracted by the assembler )
                #   - extract URL & high entropy (obfuscation) string
            elif pkg.language in ["python", "PHP"]:
                pass
                # Memo: In the case of Python & PHP, "LibrariesIO" may not provide a Download Url.
                # The Script language allows for easy string checking.
                # TODO ...
            elif pkg.language == "go":
                pass
                # Memo: In the case of GO, "LibrariesIO" may not provide a Download Url.
                # TODO ...
            elif pkg.language == "ruby":
                pass
                # TODO
                #   - download gem file (from url)
                #   - tar xvf {targetfile}.gem -C {unzip target directory}
                #   - unzip "data.tar.gz"
                #   - (The Script language allows for easy string checking.)
            elif pkg.language in ["npm", "typescript"]:
                splittedUrl = pkg.latest_download_url.split("/")
                # TODO
                #   - download library tgz file (from url)
                #   - unzip "target-library.tgz"
                #   - search `.js`, `.ts` files
                #   - (The Script language allows for easy string checking.)
            elif pkg.language == "c#":
                pass
                # TODO
                #  - download nupkg file
                #  - rename & unzip nupkg
                #  - analyze binary file...?