import sys

try:
    name_of_file = sys.argv[1]
except Exception:
    print("Uncorrect file name")
    exit(1)

convert_atom_to_solvent_radii = {"H": "1.4430",
                                 "N": "1.8300",
                                 "O": "1.7500",
                                 "C": "1.9255"}

with open(name_of_file, "r") as geom_file:
    _ = next(geom_file)
    _ = next(geom_file)
    i = 1
    outfile_lines = []
    for line in geom_file:
        atom_name = line.split()[0].upper()
        outfile_lines.append("SPHEre radius\n")
        outfile_lines.append(str(i) + " " + convert_atom_to_solvent_radii[atom_name] + "\n")
        i = i + 1

with open("solvent_radii", "w") as write_file:
    write_file.writelines(outfile_lines)


