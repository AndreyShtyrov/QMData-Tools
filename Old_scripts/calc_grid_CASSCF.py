from utils.listanalyser import ListReader
from pathlib import Path
import shutil
from utils.linalg import *
import numpy as np
from Constants.physics import MASS_CONST


def get_energy_orca(iterable):
    LR = ListReader(iterable)
    LR.go_by_keys(" ABSORPTION SPECTRUM")
    LR.get_next_lines(4)
    part = LR.get_all_by_end_and_keys("--------")
    energy_1 = float(part[0].split()[6])
    energy_2 = float(part[1].split()[6])
    foc_1 = float(part[0].split()[7])
    foc_2 = float(part[1].split()[7])
    if foc_1 > foc_2:
        return energy_1
    else:
        return energy_2

def check_term(curr_dir):
    out_file = Path(curr_dir / "opt.out")
    result = False
    if out_file.is_file():
        with open(out_file) as ch_file:
            for line in ch_file:
                if "****ORCA TERMINATED NORMALLY****" in line:
                    return True
    else:
        result = False
    return result

def creat_iteractive(path: Path):
    if not path.parent.is_dir():
        creat_iteractive(path.parent)
    if not path.is_dir():
        path.mkdir()


def make_mrci_calc(new_path, step_dir, atom_dir, old_path, temp_path):
    r_path = Path(new_path/step_dir/atom_dir)
    creat_iteractive(r_path)
    shutil.copy(str(old_path/"opt.gbw"), str(r_path/ "pr_orb.gbw"))
    shutil.copy(str(old_path/"p.3.pc"), str(r_path/"p.3.pc"))
    shutil.copy(str(temp_path), str(r_path/"opt.inp"))



if __name__ == '__main__':
    main_dir = Path.cwd()
    result = np.zeros((len([i for i in range(4, 17)]), len([i for i in range(15, 72, 5)])))
    new_path = Path.cwd()
    new_path = new_path.parent
    new_path = new_path / "20-mrci"
    for i in range(4, 17):
        atom_dir = main_dir / "atoms_{0}".format(i)
        new_atoms = "atoms_{0}".format(i)
        line = []
        for j in range(15, 72, 5):
            step_dir = atom_dir / "step_{0}".format(j)
            energy = 0.0
            if check_term(step_dir):
                new_step_dir = "step_{0}".format(j // 5)
                make_mrci_calc(new_path, new_atoms, new_step_dir, step_dir, Path.home() / "temp/template1")
                with open(str(step_dir / "opt.out"), "r") as f:
                    energy = get_energy_orca(f)
            line.append(energy)
        result[i-4, :] = np.array(line)
    grid = np.array(result)
    zero_value = 416.6
    grid = grid - zero_value
    result = []
    for i in range(grid.shape[0]):
        line = ""
        for j in range(grid.shape[1]):
            line = line + " {:.1f}".format(grid[i, j])
        line = line + " \n"
        result.append(line)
    with open(main_dir/"result.txt", "w") as f:
        f.writelines(result)


