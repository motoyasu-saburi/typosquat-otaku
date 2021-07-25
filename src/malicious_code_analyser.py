import tarfile
import tempfile
from dataclasses import dataclass
from typing import List, Optional, Tuple, T

from malicious_code_detector import MaliciousCodeDetector, MaliciousPattern

@dataclass
class MaliciousCodeAnalyseResult:
    full_code: str
    malicious_code_line: str
    code_line: int
    malicious_pattern: Tuple[str, MaliciousPattern]


@dataclass
class MaliciousCodeAnalyser:

    def _analyse_file(self, tar_file: tarfile.TarFile, file_info: List[tarfile.TarInfo], extension: str) -> List[MaliciousCodeAnalyseResult]:
        file_items: List[tarfile.TarInfo] = file_info
        filtered_file_items_info: List[tarfile.TarInfo] = self._filter_extension(extension, file_items)
        malicious_codes = []
        for file_item_info in filtered_file_items_info:
            f_info = tar_file.extractfile(file_item_info.name)
            mc_checker = MaliciousCodeDetector()
            full_code = f_info.read().decode(encoding="utf-8", errors='ignore')
            split_codes: List[str] = full_code.split("\n")
            for line_num, line in enumerate(split_codes):
                malicious_code: Optional[Tuple[str, MaliciousPattern]] = mc_checker.detect_malicious_code(line)
                if malicious_code:
                    print(malicious_code)
                    malicious_codes.append(
                        MaliciousCodeAnalyseResult(
                            full_code=full_code,
                            malicious_code_line=line,
                            code_line=line_num,
                            malicious_pattern=malicious_code
                        )
                    )
        return malicious_codes

    def _analyse_gem(self, file_path: str, extension=".rb") -> List[MaliciousCodeAnalyseResult]:
        with tarfile.open(file_path, mode="r") as gz:
            gz_members = gz.getmembers()
            # extract ruby code tar file.
            datafile_info: tarfile.TarInfo = list(filter(lambda gm: gm.name.endswith("data.tar.gz"), gz_members))[0]
            datafile = gz.extractfile(datafile_info)
            with tarfile.open(fileobj=datafile, mode="r") as datafile_gz:
                datafiles_info = datafile_gz.getmembers()
                for tf in datafiles_info:
                    print(f"      * {tf.name}")
                return self._analyse_file(tar_file=datafile_gz, file_info=datafiles_info, extension=extension)

    def _analyse_tgz(self, file_path: str, extension: str) -> List[MaliciousCodeAnalyseResult]:
        with tarfile.open(file_path, mode="r") as tgz:
            tgz_files: List[tarfile.TarInfo] = tgz.getmembers()
            filtered_files: List[tarfile.TarInfo] = self._filter_extension(extension, tgz_files)
            return self._analyse_file(tar_file=tgz, file_info=filtered_files, extension=extension)

    def _filter_extension(self, extension: str, files: List[tarfile.TarInfo]) -> List[tarfile.TarInfo]:
        return list(filter(lambda f: f.name.endswith(extension), files))

    def _filter_none(self, files: List[Optional[T]]) -> List[T]:
        return list(filter(lambda f: not f is None, files))

    def analyze(self, file_path: str, extension: str) -> List[Tuple[str, MaliciousPattern]]:
        if file_path.endswith(".tgz") or file_path.endswith(".tar"):
            return self._filter_none(self._analyse_tgz(file_path=file_path, extension=extension))
        elif file_path.endswith(".gem"):
            return self._filter_none(self._analyse_gem(file_path=file_path, extension=".rb"))
        else:
            # TODO
            return []
