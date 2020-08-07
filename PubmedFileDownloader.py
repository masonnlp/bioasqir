from ftplib import FTP
from typing import List, Tuple


class PubmedFileDownloader:

    __PUBMED_URL__ = 'ftp.ncbi.nlm.nih.gov'
    __ANNUAL_BASELINE_PATH__ = '/pubmed/baseline'
    __DAILY_BASELINE_PATH__ = '/pubmed/updatefiles/'

    def connect(self) -> bool:
        try:
            self.ftp = FTP(self.__PUBMED_URL__)
            self.ftp.login()
        except Exception:
            print("something went wrong with ftp")
            return False
        return True

    def cd_baseline(self) -> bool:
        try:
            self.ftp.cwd(self.__DAILY_BASELINE_PATH__)
        except Exception:
            print("something went wrong with ftp")
            return False
        return True

    def cd_dailyupdates(self) -> bool:
        try:
            self.ftp.cwd(self.__DAILY_BASELINE_PATH__)
        except Exception:
            print("something went wrong with ftp")
            return False
        return True

    def ls(self) -> Tuple[bool, List[str]]:
        res = []
        try:
            self.ftp.dir(lambda x: res.append(x.split(' ')[-1]))
        except Exception:
            print("something went wrong with ftp")
            return (False, res)
        return (True, res)

    def ls_ext(self, ext: str) -> Tuple[bool, List[str]]:
        files: List[str] = []
        (success, files) = self.ls()
        res = []
        if success:
            for f in files:
                if f.endswith(ext):
                    res.append(f)
            return (True, res)
        return (False, res)

    def md5_equivalent(self, fname: str):
        return fname + ".md5"

    def xml_gz_equivalent(self, fname: str):
        return fname.replace('.md5', '')

    def download_file(self, fname_src: str, fname_target: str,
                      buffer_size: int = 1000000) -> bool:
        localfile = open(fname_target, 'wb')
        try:
            self.ftp.retrbinary('RETR ' +
                                fname_src, localfile.write, buffer_size)
        except Exception:
            print("something went wrong with ftp")
            return False
        finally:
            localfile.close()
        return True

    def mass_downloader(self, target_dir: str,
                        baseline: bool = True) -> bool:
        if baseline:
            path = self.__ANNUAL_BASELINE_PATH__
        return True

