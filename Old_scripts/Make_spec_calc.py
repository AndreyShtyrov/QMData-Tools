import pathlib
import os
import shutil


def read_parametors(list_of_lines):
    mult = 1
    charge = 0
    firs_orb = 1
    last_orb = 2
    for line in list_of_lines:
        if "MULT" in line:
            mult = int(str(line).split()[-1])
        elif "CHARGE" in line:
            charge = int(str(line).split()[-1])
        elif "FIRST_ORB" in line:
            firs_orb = int(str(line).split()[-1])
            if last_orb < firs_orb:
                last_orb = firs_orb + 10
        elif "LAST_ORB" in line:
            value = int(str(line).split()[-1])
            if value > firs_orb:
                last_orb = value
            else:
                last_orb = firs_orb + 10
    return mult, charge, firs_orb, last_orb


def creat_lines_for_printing_orbitals(firs_orb, second_orb):
    result = []
    result.append("%plots\n")
    result.append("Format Gaussian_Cube\n")
    for i in range(firs_orb, second_orb +1):
        result.append("MO(\"O-" + str(i) + ".cube\"," + str(i) + ",0);\n")
    result.append("end\n")
    return result


def make_workfile(workdir, template, coords, **kwargs):
    with open(str(workdir / "opt.inp"), "w") as input:
        input.writelines(template)
        input.write("\n")
        orb_lines = creat_lines_for_printing_orbitals(first_orb, last_orb)
        input.writelines(orb_lines)
        input.write("\n")
        input.write("* xyz " + str(mult) + " " + str(charge) + "\n" )
        input.writelines(coords)
        input.write("*")


general_path = pathlib.Path.cwd()
with open(general_path.parent / "template-CEPA", "r") as temp_file:
    template_CEPA = temp_file.readlines()

with open(general_path.parent / "template-CASSCF-1", "r") as temp_file:
    template_CAS1 = temp_file.readlines()

with open(general_path.parent / "template-CASSCF-2", "r") as temp_file:
    template_CAS2 = temp_file.readlines()

with open(general_path / "coord.xyz", "r") as temp_file:
    coords = temp_file.readlines()

with open(general_path / "par", "r") as temp_file:
    par = temp_file.readlines()

mult, charge, first_orb, last_orb = read_parametors(par)

workdir = general_path / "01-CEPA"
if not workdir.is_dir():
    workdir.mkdir()
make_workfile(workdir, template_CEPA, coords, charge=charge, mult=mult, first_orb=first_orb, last_orb=last_orb)

os.chdir(str(workdir))
os.system("bash ~/bin/mORCA opt")
os.chdir(str(general_path))
if (workdir / "opt.mrci.nat").is_file():
    shutil.copy(str(workdir / "opt.mrci.nat"), str(general_path / "pr_orb.gbw"))

workdir = general_path / "02-CASSCF"
if not workdir.is_dir():
    workdir.mkdir()

make_workfile(workdir, template_CAS1, coords, charge=charge, mult=mult, first_orb=first_orb, last_orb=last_orb)
if (general_path / "pr_orb.gbw").is_file():
    shutil.copy(str(general_path / "pr_orb.gbw"), str(workdir / "pr_orb.gbw"))
os.chdir(str(workdir))
os.system("bash ~/bin/mORCA opt")
os.chdir(str(general_path))
if (workdir / "opt.gbw").is_file():
    shutil.copy(str(workdir / "opt.gbw"), str(general_path / "pr_orb.gbw"))

workdir = general_path / "03-CASSCF"
if not workdir.is_dir():
    workdir.mkdir()
make_workfile(workdir, template_CAS2, coords, charge=charge, mult=mult, first_orb=first_orb, last_orb=last_orb)

if (general_path / "pr_orb.gbw").is_file():
    shutil.copy(str(general_path / "pr_orb.gbw"), str(workdir / "pr_orb.gbw"))
os.chdir(str(workdir))
os.system("bash ~/bin/mORCA opt")
os.chdir(str(general_path))





