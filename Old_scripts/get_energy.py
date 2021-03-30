import pathlib
import numpy

key = "energy"
acc = 0
result = []
with open("from_sub1d-ADDF.xyz", "r") as input_file:
    for line in input_file:
        if "energy" in line:
            result.append(str(acc) + " " + line.split()[-1].replace(")", "") + "\n")
            acc = acc + 1

with open("result.txt", "w") as energy_file:
    energy_file.writelines(result)