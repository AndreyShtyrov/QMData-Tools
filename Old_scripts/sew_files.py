import sys, os
from pathlib import Path
import shutil

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            b = f.read()
            if b != b"":
                yield bytes(b)
            else:
                break

main_dir = os.getcwd()
#main_dir = sys.argv[1]
tmp_dirs = []

for file in os.listdir(main_dir):
    if os.path.isdir(main_dir + "/" + file):
        if "tmp_" in file:
            tmp_dirs.append(main_dir + "/" + file)
number_of_dirs = len(tmp_dirs)
with open(main_dir + "/" + "opt.ChVec1_tmp", "wb") as bin_file_ChVec1:
    for b in bytes_from_file(main_dir + "/" + "opt.ChVec1"):
        bin_file_ChVec1.write(b)
    for i in range(1, number_of_dirs + 1):
        for b in bytes_from_file(main_dir + "/tmp_"+str(i)+"/opt.ChVec1"):
            bin_file_ChVec1.write(b)
os.system("cp " + main_dir + "/" + "opt.ChVec1_tmp" + " " + main_dir + "/" + "opt.ChVec1")
