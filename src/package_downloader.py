import logging
import tempfile
from dataclasses import dataclass
from typing import List, Tuple

import requests as requests

from malicious_code_analyser import MaliciousCodeAnalyser
from libraries_io_client import LibrariesIoClient, LibrariesIoSearchResult
from malicious_code_detector import MaliciousPattern


@dataclass
class PackageDownloader:

    def download_libraries(self, keyword: str):
        lic = LibrariesIoClient()
        packages: List[LibrariesIoSearchResult] = lic.search_package(keyword)
        for pkg in packages:
            print(self.download_library(pkg))

    def download_library(self, package: LibrariesIoSearchResult) -> List[Tuple[str, MaliciousPattern]]:
        """
        :param package: download target package
        :return: downloaded file path
        """
        try:
            mca = MaliciousCodeAnalyser()  # TODO Refactoring or rename class
            print("analyse:" + package.name)
            print(f"  - URL: {package.latest_download_url}")
            if package.latest_download_url is None:
                print("")
                return []
            url_data = requests.get(package.latest_download_url).content
            splitted_url = package.latest_download_url.split("/")
            file_name = splitted_url[len(splitted_url) - 1]
            with tempfile.NamedTemporaryFile(suffix=file_name) as tf:
                tf.write(url_data)

                if package.language.lower() == "java":
                    pass
                    # Case: Binary
                    # TODO
                    #   - Download .jar
                    #   - unzip .jar
                    #   - find .class files
                    #   - javap -v target.class ( create disassembly file )
                    #   - extract comment out ( comment out is original code extracted by the assembler )
                    #   - extract URL & high entropy (obfuscation) string
                elif package.language.lower() == "go":
                    pass
                    # Memo: In the case of GO, "LibrariesIO" may not provide a Download Url.
                    # TODO ...
                elif package.language.lower() == "c#":
                    pass
                    # TODO
                    #  - download nupkg file
                    #  - rename & unzip nupkg
                    #  - DOWNLOAD FORMAT: {SCHEME}://{NUGET_DOMAIN}/api/v2/package/{PACKAGE_NAME}/{MAJOR_VERSION}.{MINOR_VERSION}
                    #  - analyze binary file...?
                elif package.language.lower() == "python":
                    # https://files.pythonhosted.org/packages/{??NUM}/{??ID}/{HASH}/{PACKAGE_NAME}-{VERSION}.tar.gz
                    # Memo: In the case, "LibrariesIO" may not provide a Download Url.
                    # The Script language allows for easy string checking.
                    pass
                elif package.language.lower() == "php":
                    # Memo: In the case, "LibrariesIO" may not provide a Download Url.
                    # The Script language allows for easy string checking.
                    pass
                elif package.language.lower() == "ruby":
                    return mca.analyze(file_path=tf.name, extension=".rb")
                    # TODO
                    #  (maybe) unzip "tar.gz"
                elif package.language.lower() == "npm":
                    # https://registry.npmjs.org/{package-name}/-/{package-name}-{version}.tgz
                    return mca.analyze(file_path=tf.name, extension=".js")
                elif package.language.lower() == "typescript":
                    return mca.analyze(file_path=tf.name, extension=".ts")

        except Exception as e:
            logging.error(e)