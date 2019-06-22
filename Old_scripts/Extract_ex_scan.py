import pathlib
import numpy as np
dict_of_res = []
general_dir = pathlib.Path.cwd()

for cdir in general_dir.iterdir():
    name = cdir.name
    list_of_val = []
    dist = cdir / "opt.log"
    print(name)
    if dist.is_file() and "step" in cdir.name:
        pos = int(name.split("-")[0])
        with open(str(cdir / "opt.log"), "r") as input_file:
            for line in input_file:
                if "Final state energy(ies):" in line:
                    break
            _ = next(input_file)
            _ = next(input_file)
            for line in input_file:
                try:
                    list_of_val.append(float(line.split()[-1]))
                except:
                    break
        dict_of_res.insert(pos, list_of_val)
list_of_lines = ["" for i in range(len(dict_of_res[0]))]
for res in dict_of_res:
    for j in range(len(list_of_lines)):
        list_of_lines[j] = list_of_lines[j] + " " + str(res[j])
for j in range(len(list_of_lines)):
    list_of_lines[j] = list_of_lines[j] + " \n"
with open("result.txt", "w") as outfile:
    outfile.writelines(list_of_lines)





