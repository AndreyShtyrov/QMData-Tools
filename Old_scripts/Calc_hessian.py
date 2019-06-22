import pathlib
import numpy as np
import shutil

def save_geom_xyz(charges: list, coords, comment = ""):
    result = []
    n_atoms = len(charges)
    result.append(str(n_atoms) + "\n")
    result.append(comment + "\n")
    for j in range(n_atoms):
        line = charges[j] + " "
        line = line + "{:>15.7f}".format(coords[3 * j])
        line = line + "{:>15.7f}".format(coords[3 * j + 1])
        line = line + "{:>15.7f}".format(coords[3 * j + 2])
        line = line + "\n"
        result.append(line)
    return result

convector_const = 1.889725989
general_path = pathlib.Path.cwd()
with open(general_path / "coord.xyz", "r") as coord_file:
    line = next(coord_file)
    line.replace("\n","")
    n_atoms = int(line)
    _ = next(coord_file)
    charges = []
    xyz_coord = []
    for line in coord_file:
        charges.append(line.split()[0])
        xyz_coord.extend(map(float, line.split()[1:]))
    xyz_coord = np.array(xyz_coord)
    xyz_coord_in_borh = xyz_coord * convector_const

work_dir = general_path / "hessian_step00"
if work_dir.is_dir():
    shutil.rmtree(str(work_dir))
    work_dir.mkdir()
else:
    work_dir.mkdir()
shutil.copy(str(general_path/"template"), str(work_dir/ "opt.input"))
shutil.copy(str(general_path/"pr_orb.RasOrb"), str(work_dir/ "pr_orb.RasOrb"))
coord_lines = save_geom_xyz(charges, xyz_coord)
with open(str(work_dir / "opt.xyz"), "w") as coord_file:
    coord_file.writelines(coord_lines)

for i in range(1, 3 * n_atoms + 1):
    for sign in [-1, 1]:
        work_dir = general_path / ("hessian_step" + str(sign * i))
        if work_dir.is_dir():
            shutil.rmtree(str(work_dir))
            work_dir.mkdir()
        else:
            work_dir.mkdir()
        shutil.copy(str(general_path/"template"), str(work_dir/ "opt.input"))
        shutil.copy(str(general_path/"pr_orb.RasOrb"), str(work_dir/ "pr_orb.RasOrb"))
        with open(str(work_dir / "opt.xyz"), "w") as coord_file:
            shift = np.zeros(3*n_atoms)
            shift[i-1] = sign * 0.01
            local_geom = xyz_coord + shift
            local_geom = local_geom / convector_const
            coord_lines = save_geom_xyz(charges, local_geom)
            coord_file.writelines(coord_lines)





