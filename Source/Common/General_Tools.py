import numpy as np

def read_xyz(file):
    """

    :param file: path to file with xyz geom
    :return: tuple (charges, coords :ndarray 1 dimetional)
    """
    with open(file, "r") as f:
        charges = []
        coords = []
        try:
            line = next(f)
            if line.replace("\n", "").isdigit():
                line = next(f)
            else:
                charges.append(int(line.split()[0]))
                coords.extend([float(x) for x in line.split()[1:]])
        except StopIteration:
            print("coord file is empty")
            exit(2)
        for line in f:
            line.replace("\n", "")
            charges.append(int(line.split()[0]))
            coords.extend([float(x) for x in line.split()[1:]])

        return np.array(charges), np.array(coords)

def save_geom_xyz(charges: list, coords, comment = ""):
    result = []
    n_atoms = len(charges)
    if comment is not "":
        result.append(str(n_atoms) + "\n")
        result.append(comment + "\n")
    for j in range(n_atoms):
        line = str(charges[j]) + " "
        line = line + "{:>15.7f}".format(coords[3 * j])
        line = line + "{:>15.7f}".format(coords[3 * j + 1])
        line = line + "{:>15.7f}".format(coords[3 * j + 2])
        line = line + "\n"
        result.append(line)
    return result