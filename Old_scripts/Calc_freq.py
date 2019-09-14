import numpy as np
import numpy.linalg as lg
from Source.Utils import *
from Source.Constants.physics import MASS_CONST

convector_const = 1.889725989
MAU_CONST = 9.109389e-31
HART_CONST = 627.5


def read_coord():
    with open("coord.xyz", "r") as coord_file:
        n_atoms = int(next(coord_file).replace("\n", ""))
        _ = next(coord_file)
        charges = []
        coords = []
        for line in coord_file:
            charges.append(line.split()[0].upper())
            coords.extend(map(float, line.replace("\n", "").split()[1:]))
        return charges, np.array(coords) * convector_const

def read_hessian(charges):
    listanalizer = ListAnalyser()
    with open("freq.fchk", "r") as freq_file:
        iterable = iter(freq_file)
        listanalizer._go_by_keys(iterable, "Cartesian Force Constants")
        hess_file = iter(listanalizer._get_all_by_keys(iterable, "Dipole Moment"))

        hess_values = []
        while len(hess_values) != 3 * len(charges) * (3 * len(charges) + 1) // 2:
            s = next(hess_file)
            hess_values.extend(map(float, s.split()))

        hess_values_iter = iter(hess_values)

        hess = np.zeros((3 * len(charges), 3 * len(charges)))
        for i in range(3 * len(charges)):
            for j in range(0, i + 1):
                hess[i, j] = hess[j, i] = next(hess_values_iter)
    return hess

if __name__ == '__main__':

    charges, coords = read_coord()
    hessian = read_hessian(charges)
    hessian = hessian

    masses = [MASS_CONST[i] for i in charges]
    d = np.zeros(len(masses) * 3)
    for i in range(3):
        d[i::3] = np.sqrt(masses)


    for i in range(len(charges)*3):
        for j in range(len(charges)*3):
            #print(str(int(i/3)) + " : " + str(i))
            hessian[i, j] = hessian[i, j]/(math.sqrt(MASS_CONST[charges[int(i/3)]]) * math.sqrt(MASS_CONST[charges[int(j/3)]]))
            pass

    new_basis = internal_coords(coords, [MASS_CONST[i] for i in charges], charges)

    hess = new_basis.T.dot(hessian).dot(new_basis)

    s, u = lg.eigh(hess)
    normal_modes = new_basis.dot(u)

    s = s * 627.5 * convector_const ** 2 * 4184 / (10 ** 5 * 6.022)
    freq = []

    for fr in s:
        if fr < 0:
            freq.append(-1 * math.sqrt(-fr) * 1302.79)
        else:
            freq.append(math.sqrt(fr) * 1302.79)
    print(len(freq))

    with open("freq.txt", "w") as freq_file:
        for fr in freq:
            freq_file.write(str(fr) + "\n")
    print(freq)
    print("**********")

    factor_list = []
    for i in range(normal_modes.shape[1]):
        normal_modes[:, i] = normal_modes[:, i] / d
#        print(normal_modes[:, i])
        factor = sum(map(lambda x: x ** 2, normal_modes[:, i]))
        factor = 1 / factor
        factor_list.append(factor)
        normal_modes = normal_modes[:, i] * math.sqrt(factor)
        print(normal_modes[:, i] * math.sqrt(factor))
        print(factor)
        print(freq[i])
        print("***")

