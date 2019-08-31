import pathlib
import os


def count_dirs(path: pathlib.Path):
    i = 0
    for dir in path.iterdir():
        if dir.is_dir():
            i = i + 1
    return i

if __name__ == '__main__':
    m = 4
    main_path = pathlib.Path.cwd()
    n_dirs = count_dirs(main_path)
    j = 0
    i = 0
    n = n_dirs % m
    for dir in main_path.iterdir():
        if dir.is_dir():
            if j == 0:
                os.system("tar -cvf run" + str(i) + ".tar" + str(dir))
            elif 0 < j < n:
                os.system("tar -rvf run" + str(i) + ".tar" + str(dir))
            elif j == n:
                os.system("tar -rvf run" + str(i) + ".tar" + str(dir))
                i = i + 1
                j = 0
