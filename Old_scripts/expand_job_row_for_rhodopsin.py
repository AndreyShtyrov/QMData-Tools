from pathlib import Path
import numpy as np
import os


def find_max_min(cur_path):
    min = 100
    max = 0
    for cdir in cur_path.iterdir():
        index = int(cdir.name.replace("st", ""))
        if index < min:
            min = index
        if index > max:
            max = index
    return max, min

def get_vector1(inp_file, inp_file1):
    with open(inp_file / "p.3.pc", "r") as input_file:
        _ = next(input_file)
        v1 = next(input_file).split()[1:]
        v1 = [float(i) for i in v1]
        v1 = np.array(v1)
    with open(inp_file1 / "p.3.pc", "r") as input_file:
        _ = next(input_file)
        v2 = next(input_file).split()[1:]
        v2 = [float(i) for i in v2]
        v2 = np.array(v2)
    return v1 - v2, v1
def get_vector2(inp_file, inp_file1):
    with open(inp_file / "p.3.pc", "r") as input_file:
        _ = next(input_file)
        _ = next(input_file)
        v1 = next(input_file).split()[1:]
        v1 = [float(i) for i in v1]
        v1 = np.array(v1)
    with open(inp_file1 / "p.3.pc", "r") as input_file:
        _ = next(input_file)
        _ = next(input_file)
        v2 = next(input_file).split()[1:]
        v2 = [float(i) for i in v2]
        v2 = np.array(v2)
    return v1 - v2, v1

def create_new_inp(max, cur_path):
    charge = "-1.0 "
    for i in range(1, 7):
        new_dir = cur_path
        new_dir.mkdir(exist_ok=True)
        new_dir2 = cur_path / ("st" + str(max + i))
        dir_w_temp = cur_path / ("st" + str(max))
        dir_w_temp1 = cur_path / ("st" + str(max - 1))
        shift, v1 = get_vector1(dir_w_temp, dir_w_temp1)
        new_coor = shift + v1 * i
        # shift, v1 = get_vector2(dir_w_temp, dir_w_temp1)
        # new_coor1 = shift + v1 * i
        new_dir2.mkdir(exist_ok=True)
        os.system("cp " + str(dir_w_temp /"pr_orb.gbw") + " " + str(new_dir2 / "pr_orb.gbw"))
        os.system("cp " + str(dir_w_temp / "opt.inp") + " " + str(new_dir2))
        with open(new_dir2/"p.3.pc", "w") as point_charge_file:
            point_charge_file.write(" 2\n")
            line = "-1.0" + "{:>12.4f}".format(new_coor[0])
            line = line + "{:>12.4f}".format(new_coor[1])
            line = line + "{:>12.4f}".format(new_coor[2]) + "\n"
            point_charge_file.write(line)
                # line = "-0.43" + "{:>12.4f}".format(new_coor1[0])
                # line = line + "{:>12.4f}".format(new_coor1[1])
                # line = line + "{:>12.4f}".format(new_coor1[2]) + "\n"
                # point_charge_file.write(line)

cur_path = Path.cwd()
max, min = find_max_min(Path("atom-4"))
for cdir in cur_path.iterdir():
    if cdir.is_dir():
        create_new_inp(max, cdir)


from pathlib import Path
import os
def iter_dir_by_template(template : str,cur_dir: Path):
    for dir in cur_dir.iterdir():
        if dir.is_dir():
            yield from iter_dir_by_template(template, dir)
        elif dir.is_file():
            if template in str(dir):
                yield dir

cur_dir = Path.cwd()
iter_files = iter_dir_by_template("/opt.inp", cur_dir)
for cfile in iter_files:
    trigger = True
    print(str(cfile))
    outfile = cfile.parent / "opt.out"
    if outfile.is_file():
        with open(outfile, "r") as inputfile:
            for line in inputfile:
                if "****ORCA TERMINATED NORMALLY****" in line:
                    trigger = False
                    break
    if trigger:
        os.chdir(str(cfile.parent))
        os.system("cp ~/input opt.inp")
        os.system("bash ~/bin/mORCA3 opt")
        os.chdir(str(cur_dir))