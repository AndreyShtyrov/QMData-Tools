import pathlib
import shutil
import math

def convert_int_in_format_for_system(number: int, min_len) -> str:
    result = str(number)
    for i in range(1, min_len):
        if number < 10 ** i:
            result = str(0) + result
    return result

def get_first_last_and_dict_of_dirs(general_path):
    dir_dictionary = {}
    max_key = 0
    first_key = -1
    for dir in general_path.iterdir():
        if dir.is_dir() and "-" in dir.name:
            number = dir.name.split("-")[0]
            number = int(number)
            dir_dictionary.update({number: dir})
            if first_key == -1:
                first_key = number
            if number > max_key:
                max_key = number
            elif number < first_key:
                first_key = number
    return first_key, max_key, dir_dictionary


def reverse_directories():
    general_path = pathlib.Path.cwd()
    first_key, max_key, dir_dictionary = get_first_last_and_dict_of_dirs(general_path)
    final_path = general_path / "new_dirs"
    final_path.mkdir()
    for ndir in range(first_key, max_key + 1):
        new_number = max_key - ndir
        new_dir = final_path / (convert_int_in_format_for_system(new_number, 2) + "-step" + str(new_number))
        shutil.move(dir_dictionary[ndir], new_dir)

import pathlib


def make_scan(orb_temp_name: str):
    general_path = pathlib.Path.cwd()
    with open(general_path / "template", "r") as tmp_file:
        template = tmp_file.readlines()
    first_key, max_key, dir_dictionary = get_first_last_and_dict_of_dirs(general_path)
    prev_dir = general_path / "orb"
    for i in range(first_key, max_key):
        with open(dir_dictionary[i] / "opt.input", "w") as inp_file:
            line = ">>COPY $InpDir/../" + prev_dir.name + "/" + orb_temp_name + " $WorkDir/INPORB"
            inp_file.write(line + "\n")
            inp_file.writelines(template)
        prev_dir = dir_dictionary[i]


if __name__ == '__main__':
    make_scan("INPORB")


