from dataclasses import dataclass
from typing import List, Tuple, Optional

from package_downloader import PackageDownloader


def main():
    pd = PackageDownloader()
    pd.download_libraries("python")


if __name__ == '__main__':
    main()

