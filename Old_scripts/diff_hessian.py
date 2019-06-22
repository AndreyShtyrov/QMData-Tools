import pathlib
import numpy as np
from utils.molecul_property import read_coord

charges, coords = read_coord()
n_dims = len(charges) * 3

def read_force(file, ndims):
    result = []
    print(file)
    with open(file, "r") as grad_file:
        for line in grad_file:
            if "*              Molecular gradients" in line:
                break
        for _ in range(7):
            line = next(grad_file)
        for i in range(int(n_dims/3)):
            line = next(grad_file)
            result.extend(map(float, line.replace("\n", "").split()[1:]))
    return np.array(result)

t_shift = 0.02
template = "hessian_step"
hessian = np.zeros((n_dims, n_dims))
list_neg_g = []
list_pos_g = []

for i in range(n_dims):
    grad = read_force(template + str(-(i+1)) + "/opt.log", n_dims)
    list_neg_g.append(np.array(grad))
    grad = read_force(template + str(i+1) + "/opt.log", n_dims)
    list_pos_g.append(np.array(grad))
for i in range(n_dims):
    for j in range(n_dims):
        hessian[i,j] = 0.5 * ((list_pos_g[i][j] - list_neg_g[i][j])/ t_shift  + (list_pos_g[j][i] - list_neg_g[j][i])/ t_shift)
hessian = hessian * (0.41999/0.420285)
with open("hess.txt", "w") as write_file:
    line = ""
    for i in range(n_dims):
        for j in range(i + 1):
            if len(line.split()) < 4:
                line = line + str(hessian[i,j]) + " "
            else:
                line = line + str(hessian[i,j]) + "\n"
                write_file.write(line)
                line = ""
    if not line is "":
        write_file.write(line + "\n")
