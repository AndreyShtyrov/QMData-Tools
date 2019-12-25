import json
import pathlib
from typing import Union
import shutil
import hashlib
import yaml
from Source.Common.Data import data

import clipboard
import os
import time
import zipfile


def get_dir_tree(curr_path: pathlib.Path):
    for file in curr_path.iterdir():
        if file.is_dir():
            yield from get_dir_tree(file)
        elif file.is_file():
            yield file
    return


def treatment_exception(error: Exception):
    if error is PermissionError:
        return False

def convert_str_to_dict(line: str) -> dict:
    result = dict()
    for part in line.split(";")[:-1]:
        result.update({part.split(":")[0]: part.split(":")[1]})
    return result

def load_from_clipboard(path: pathlib.Path):
    data = clipboard.paste()
    data = convert_str_to_dict(data)
    if "geom" in data.keys():
        prev_geom: str = data["geom"]
        shutil.copy(prev_geom, str(path.absolute()))
    if "orb" in data.keys():
        prev_path: str = data["orbitale"]
        extension = prev_path.split(".")[-1]
        shutil.copy(prev_path, str(path / ("pr_orb." + extension)))


def save_in_clipboard(path: pathlib.Path):
    result = ""
    for file in path.iterdir():
        if file.is_file():
            if file.name == "coord.xyz":
                result = "geom:" + str(file.absolute()) + ";"
            elif ".gbw" in file.name or "RasOrb" in file.name:
                result.update("orb:" + str(file.absolute()) + ";")
    clipboard.copy(result)


def make_dir_forced(curr_dir: pathlib.Path)-> None:
    if curr_dir.parent.is_dir():
        make_dir_forced(curr_dir.parent)
    else:
        curr_dir.mkdir()


def get_dir_tree_list(curr_path: pathlib.Path):
    result = []
    for file in get_dir_tree(curr_path):
        result.append(file)
    return result


def search_file_with_template_in_name(curr_path: pathlib.Path, template: str) -> Union[pathlib.Path, bool]:
    try:
        return _search_file_with_template_in_name(curr_path, template)
    except PermissionError:
        return False


def _search_file_with_template_in_name(curr_path: pathlib.Path, template: str) -> Union[pathlib.Path, bool]:
    main_dir = pathlib.Path.home()
    for file in curr_path.iterdir():
        if file.is_file():
            if template in file.name:
                return file
    if main_dir != curr_path:
        if curr_path.parent.is_dir():
            return search_file_with_template_in_name(curr_path.parent, template)
    return False


class dir_cash(data):
    def __init__(self, dir: pathlib.Path):
        self.name = str(dir.absolute())
        self.dir = dir
        self.cash_file = dir / "cash.json"
        self.path_saved = dir / ".prev_states"
        if self.cash_file.is_file():
            self.cash = self._load_json(self.cash_file)
        else:
            shutil.rmtree(str(self.path_saved))
            self.cash = list
            self.save_state()

    def save_state(self):
        hash = hashlib.md5(self.name)
        t = time.clock()
        changes = self.zip_files(str(hash) + str(t) + ".zip", self.dir)
        state = {"id": hash,
                 "time": t,
                 "changes": changes,
                 "machine": self.get_cluster_name()}
        self.cash.append(state)

    def load(self) -> list:
        return self._load_json(self.cash_file)

    def save(self):
        self._save_json(self.cash_file, self.cash)

    def get_cluster_name(self):
        cluster = self._load_json(pathlib.Path.home() / ".cluster_data")
        return cluster["name"]

    def zip_files(self, name, dir: pathlib.Path):
        changes = dict
        archive = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
        for file in dir.iterdir():
            if file.is_file():
                archive.write(str(file))
                changes.update({file.name: os.path.getctime(str(file))})
        archive.close()
        return changes

    def unzip_files(self, name):
        zipfile.ZipFile.extract(name)


class config_file():
    def load_file(self, path):
        with open(path, "r") as steam:
            file = yaml.load(steam)
        return file

    def save_file(self, path: pathlib.Path, config):
        data = yaml.dump(config, indent=2, default_flow_style=False)
        path.write_text(data)


def changes(data):
    def __init__(self, load_data):
        self.name = load_data['name']

