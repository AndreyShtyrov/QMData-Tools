import pathlib
from pathlib import Path
import numpy as np
from Source.Utils.listanalyser import ListReader


def check_term(curr_dir) -> bool:
    out_file = pathlib.Path(curr_dir / "opt.out")
    result = False
    if out_file.is_file():
        with open(out_file) as ch_file:
            for line in ch_file:
                if "****ORCA TERMINATED NORMALLY****" in line:
                    return True
    else:
        result = False
    return result

def get_mrci_spectr(iterable):
    LR = ListReader(iterable)
    LR.go_by_keys("CI-EXCITATION SPECTRA")
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

if __name__ == '__main__':
    main_dir = Path.cwd()
    result = np.zeros((len([i for i in range(4, 17)]), len([i for i in range(3, 13)])))
    result1 = np.zeros((len([i for i in range(4, 17)]), len([i for i in range(3, 13)])))
    new_path = Path.cwd()
    new_path = new_path.parent
    new_path = new_path / "20-mrci"
    for i in range(4, 17):
        atom_dir = main_dir / "atoms_{0}".format(i)
        new_atoms = "atoms_{0}".format(i)
        line = []
        line2 = []
        for j in range(3, 13):
            step_dir = atom_dir / "step_{0}".format(j)
            energy = 0.0
            energy_cas = -1000
            if check_term(step_dir):
                new_step_dir = "step_{0}".format(j)
                with open(str(step_dir / "opt.out"), "r") as f:
                    energy_cas = get_energy_orca(f)
                    energy = get_mrci_spectr(f)
            line.append(energy)
            line2.append(energy_cas-energy)
        result[i - 4, :] = np.array(line)
        result1[i-4, :] =np.array(line2)
    grid = np.array(result)
    grid1 = np.array(result1)
    zero_value = 595.5
    grid = grid - zero_value

    result = []
    result1 = []
    for i in range(grid.shape[0]):
        line = "atom_"  + str(i + 4)
        for j in range(grid.shape[1]):
            line = line + " {:.1f}".format(grid[i, j])
        line = line + " \n"
        result.append(line)
    for i in range(grid1.shape[0]):
        line = "atom_"  + str(i + 4)
        for j in range(grid1.shape[1]):
            line = line + " {:.1f}".format(grid1[i, j])
        line = line + " \n"
        result1.append(line)
    with open(main_dir/"result.txt", "w") as f:
        f.writelines(result)
    with open(main_dir / "result1.txt", "w") as f:
        f.writelines(result1)