import sys, os
import shutil

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
                else:
                    break

main_dir = sys.argv[1]
tmp_dirs = []

for file in os.listdir(main_dir):
    if os.path.isfile(main_dir + "/" + file):
        if "tmp_" in file:
            tmp_dirs.append(main_dir + "/" + file)
number_of_dirs = len(tmp_dirs)
with open(main_dir + "/" + "opt.ChVec1_tmp", "wb") as bin_file_ChVec1:
    for b in bytes_from_file(main_dir + "/" + "opt.ChVec1", "wb"):
        bin_file_ChVec1.write(b)
    for i in range(1, number_of_dirs):
        for b in bytes_from_file(main_dir + "/tmp_"+str(i)+"/opt.ChVec1"):
            bin_file_ChVec1.write(b)
os.system("cp " + main_dir + "/" + "opt.ChVec1_tmp" + " " + main_dir + "/" + "opt.ChVec1")


string = sys.argv[2]
string_components = string.split("/")
last_string_index = len(string_components) - 1
string_components.insert(last_string_index, "add_modules")
new_string = ""
for string_component in string_components:
    new_string = new_string + "/" + string_component
iterable = sys.argv
_ = next(iterable)
_ = next(iterable)
for component in iterable:
    new_string = new_string + " " + component
print(new_string)
main_dir = sys.argv[1]
tmp_dirs = []





