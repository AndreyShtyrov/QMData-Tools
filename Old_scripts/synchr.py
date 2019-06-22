import os
import zipfile
from time import time
import datetime


class sync():
    def __init__(self, main_path):
        self._main_path = main_path
        self._all_paths = []
        self._all_paths.append(self._main_path)
        self._all_files = []
        self.get_all_tree()
        self._avail_formats = [".inp",  "00-propertyes", "Fors.chk", "requst", "opt.xyz", "struct.xyz", "struct1.xyz", "struct2.xyz",
                               "opt.hess", "orb.chk", ".json", "start.molden", "start.arch"]
        self.name_cluster = "computer"


    def _get_all_dir(self,path):
        result = []
        dirs = os.listdir(path)
        for dir in dirs:
            if os.path.isdir(path + "/" + dir):
                result.append(path + "/" + dir)
        return  result

    def _get_all_files(self, path):
        result  = []
        files = os.listdir(path)
        for file in files:
            if os.path.isfile(path + "/" + file):
                result.append(path + "/" + file)
        return  result

    def _is_there_dirs(self):
        for path in self._all_paths:
            os.listdir(path)
            components = os.listdir(path)
            for component in components:
                if os.path.isdir(path + "/" + component) and  not(path + "/" + component in self._all_paths):
                    return True
        return False

    def get_all_tree(self):
        while self._is_there_dirs():
            for path in self._all_paths:
                self._all_paths.extend(self._get_all_dir(path))
        for path in self._all_paths:
            self._all_files.extend(self._get_all_files(path))

    def _check_format(self, file):
        if not(self.name_cluster == "computer"):
            return True
        else:
            for a in self._avail_formats:
                if a in file:
                    return True
            return False

    def get_all_changed_files(self):
        result = []
        for file in self._all_files:
            #print(file)
            if self._check_format(file):
                    result.append(file)
                    #print(file)
        return result

    def make_archive(self):
        zipf = zipfile.ZipFile(os.getcwd() + '/' + self.name_cluster + '.zip', 'w', zipfile.ZIP_DEFLATED)
        files = self.get_all_changed_files()
        if os.path.isfile(self._main_path + '/requst'):
            for file in files:
                #print(file)
                if not("time.txt" in file):
                    print(file)
                    zipf.write(file.replace(os.getcwd() + "/", ""))





if __name__ == '__main__':
    with open(".sync.txt", "r") as syncdirs:
        for syncdir in syncdirs:
            sync = sync(syncdir.replace("\n", ""))
            sync.make_archive()

