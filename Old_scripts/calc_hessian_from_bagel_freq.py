import numpy as np
from Source.ReaNet import reanet_parser
from Source.Utils.listanalyser import ListReader
import math
def get_geometry_from_bagel(iterable):
    LR = ListReader(iterable)
    LR.go_by_keys("*** Geometry ***")
    LR.get_next_lines(1)
    part_of_file = LR.get_all_by_keys(" The gradients will be computed analytically.")
    coord = []
    for line in part_of_file:
        line = line.replace(",", "")
        if len(line.split()) < 4:
            break
        coord.extend([float(i) for i in line.split()[7:10]])
    LR.go_by_keys("* Nuclear energy gradient")
    LR.get_next_lines(1)
    part_of_file = LR.get_all_by_keys("* Gradient computed with")
    grads = []
    for line in part_of_file:
        line = line.replace("\n", "")
        if " x " in line or " y " in line or " z " in line:
            grads.append(float(line.replace("\n", "").split()[-1]))
    return np.array(coord), np.array(grads)


def get_hessian(iterable):
    LR = ListReader(iterable)
    LR.go_by_keys("++ Symmetrized Mass Weighted Hessian ++")
    LR.get_next_lines(2)
    part = LR.get_all_by_keys("* Projecting out translational and rotational degrees of freedom", "Mass Weighted Hessian Eigenvalues")
    temporary = []
    for line in part:
        try:
            [int(i) for i in line.replace("\n", "").split()[3]]
        except IndexError:
            pass
        except ValueError:
            if not "* Vibrational frequencies, " in line:
                if "averaged" in line:
                    print(1)
                temporary.append([float(i) for i in line.replace("\n", "").split()[1:]])
    ndim = int(math.sqrt((len(temporary)-1) * 6 + len(temporary[-1])))
    hessian = np.zeros((ndim, ndim))
    for i in range(len(temporary)):
        for j in range(len(temporary[i])):
            index1 = (i // ndim) * 6
            index2 = (i % ndim)
            hessian[index1 + j, index2] = temporary[i][j]
    return np.array(hessian)


def get_section_with_grad_iter(path_to_file):
    with open(path_to_file) as input_file:
        LR = ListReader(input_file)
        LR.go_by_keys("Since a DF basis is specified, we compute 2- and 3-index integrals:")
        while True:
            result = LR.get_all_by_end_and_keys("Since a DF basis is specified, we compute 2- and 3-index integrals:")
            if result:
                yield result
            else:
                break

if __name__ == '__main__':
    def old_body():
        with open("save_start", "r")as initial:
            coord, grads = get_geometry_from_bagel(initial)
        zero_grad = grads
        path_to_file = "freq.log"
        coord_array = []
        grads_array = []
        for part in get_section_with_grad_iter(path_to_file):
            coord, grads = get_geometry_from_bagel(part)
            coord_array.append(coord)
            grads_array.append(grads)
        zero_coord = coord_array[0]
        result = np.zeros_like(len(zero_coord))
        for coord in coord_array:
            result = abs(coord - zero_coord) + result
        print(result)
        print(zero_coord[0:3]/1.88972585931612435672)

    with open("opt.out", "r") as hessian_file:
        hessian = get_hessian(hessian_file)
        reanet_parser.save_hessian("hessian.txt", hessian)
