#!/usr/bin/env python
import os, sys
from pathlib import path


type_of_calculation = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

os.environ["molpro_dir"]="/usr/local/molpro/molprop_2010_1_linux_x86_64_i8/bin"

path = path.cwd()
main_dir = path.parent.parent

lines_of_input_file = []


with open( main_dir / "head_of_input", "r") as head_of_input:
    lines_of_input_file.extend(head_of_input.readlines())
lines_of_input_file.append("geometry={angstrom;\n")

number_of_atoms = len(lines_of_input_file)
with open("input.xyz") as coord_file:
    iterator = iter(coord_file.readlines())
    _ = next(iterator)
    _ = next(iterator)
    lines_of_input_file.extend(iterator)

number_of_atoms = len(lines_of_input_file) - number_of_atoms
lines_of_input_file.append("}\n")


if type_of_calculation == "energy":
    with open( main_dir / "energy_input", "r") as energ_file:
        lines_of_input_file.extend(energ_file.readlines())
elif type_of_calculation == "grad":
    with open( main_dir / "grad_input") as grad_file:
        lines_of_input_file.extend(grad_file.readlines())
elif type_of_calculation == "hess":
    with open( main_dir / "hess_input") as hess_file:
        lines_of_input_file.extend(hess_file.readlines())
with open(path / "input", "w") as input_file:
    input_file.writelines(lines_of_input_file)
os.system("cp ../../tmp/140719771879232/output .")
#os.system("$molpro_dir/molpro  -o output input")
with open(path / "output", "r") as output_file:
    line_iterator = iter(output_file.readlines())
for line in line_iterator:
    if "!rspt2 state 1.1 energy" in line:
        energy = float(line.replace("\n","").split()[-1])
        break
if type_of_calculation == "grad":
    gradient = []
    for line in line_iterator:
        if "rspt2 gradient for state 1.1" in line:
            break
    _ = next(line_iterator)
    _ = next(line_iterator)
    _ = next(line_iterator)
    for i in range(number_of_atoms):
        line = next(line_iterator)
        xyz_gradient = line.replace("\n", "").split()[1:]
        grad = ""
        for component in xyz_gradient:
            grad = grad + component + "  "
        grad = grad + "\n"
        gradient.append(grad)

if type_of_calculation == "hess":
    hessian = []
    for line in line_iterator:
        if "" in line:
            break
    _ = next(line_iterator)
    for i in line_iterator:
        if len(i.split()) > 1:
            i.replace("\n", "")

lines_of_output_file = []
lines_of_input_file.append(str(energy) + " \n")
lines_of_output_file.extend(gradient)

with open(path / "chk.fchk", "w") as chk_file:
    chk_file.writelines(lines_of_output_file)


