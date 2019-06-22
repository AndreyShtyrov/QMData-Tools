import os
import sys
import pathlib
from .listanalyser import ListAnalyser


class parser(ListAnalyser):

    def __init__(self, file_name):
        super().__init__()
        self._list_of_lines = []
        with open(file_name, "r") as out_file:
            self._list_of_lines.extend(map(lambda line: line.replace("\n", ""), out_file.readlines()))
        self.iterable = iter(self._list_of_lines)
        self.last_line = None

    def get_all(self):
        return self._list_of_lines

    def go_to_key(self, *keys):
        try:
            self.last_line = self._go_by_keys(self.iterable, *keys)
        except StopIteration:
            self.parser_exception("End_of_file")

    def get_all_by_keys_and_end(self, *keys):
        result = self._get_all_by_end_and_keys(self, self.iterable, *keys)
        self.reset_iters()
        return result

    def get_all_by_key(self, *keys):
        try:
            result = self._get_all_by_keys(self.iterable, *keys)
            self.last_line = result[-1]
            return result
        except StopIteration:
            self.parser_exception("End_of_file")

    def get_part_of_file(self, start_keys, stop_keys):
        try:
            iterator = self._yield_part(self.iterable, start_keys, stop_keys)
            yield from iterator
        except StopIteration:
            self.parser_exception("End_of_file")

    def parser_exception(self, exception_name):
        if exception_name is 'End_of_file':
            self.reset_iters()
            raise StopIteration

    def reset_iters(self):
        self.iterable = iter(self._list_of_lines)
        self.last_line = None


def get_dir_tree(path) -> pathlib.Path:
    if not type(path) is pathlib.Path:
        try:
            path = pathlib.Path("./path")
        except TypeError:
            print("it is not string")
            exit(1)
    for cur_dir in path.iterdir():
        if not cur_dir.is_dir():
            yield cur_dir
        else:
            yield from get_dir_tree(cur_dir)
    return 


