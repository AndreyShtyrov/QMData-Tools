import pathlib
import os, sys

try:
    line = sys.argv[1]
except IndexError:
    exit()

line = line.split("_scratch/")[1]
print(line)
