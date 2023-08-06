import os

from texta_parsers.tools.extension import Extension


class DocScanner:

    def __init__(self):
        self.scanned_files_path = os.path.join(os.getcwd(), "scanned_files.txt")
        self.scanned_files = self._get_scanned_files()


    def scan(self, directory):
        """
        Scans directory and all its subdirectories.
        All paths for found (and supported) files are yielded.
        """
        batch = []
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                abspath = os.path.abspath(file_path)
                print(abspath)
                if abspath not in self.scanned_files:
                    self._save_path(abspath)
                    print(abspath)
                    if Extension.is_supported(abspath):
                        yield abspath


    def _save_path(self, path):
        """
        Saves seen paths to file.
        """
        with open(self.scanned_files_path, "a") as f:
            self.scanned_files[path] = True
            f.write(f"{path}\n")


    def _get_scanned_files(self):
        """
        Retrieves saved paths fron file.
        """
        if(os.path.isfile(self.scanned_files_path) == True):
            with open(self.scanned_files_path, "r") as f:
                files_dict = {path.strip(): True for path in f.readlines() if path}
            return files_dict
        else:
            return {}


    def remove_scanned_file(self):
        """
        Deletes file containing scanned paths.
        """
        if os.path.isfile(self.scanned_files_path):
            os.remove(self.scanned_files_path)
