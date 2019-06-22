import numpy as np
import numpy.linalg as lg
import math
from Constants.physics import MASS_CONST


def separete_basis(first_part):
    """
    Принимает на вход набор векторов, а затем достраивает систему до базиса с помощью процесса Грама-Шмидта

    :param first_part: набор векторов в виде матрицы nxk, где k - количество векторов, n - их размерность
    :return: ортонормированный базис
    """
    n_dims = first_part.shape[0]
    basis = np.zeros((n_dims, n_dims))
    basis[:, :first_part.shape[1]] = first_part
    basis[:, first_part.shape[1]:] = np.random.randn(n_dims, n_dims - first_part.shape[1])
    basis, r = np.linalg.qr(basis)
    return basis

def vector_mult(vector1, vecort2):
    x = vector1[1] * vecort2[2] - vector1[2] * vecort2[1]
    y = vector1[2] * vecort2[0] - vector1[0] * vecort2[2]
    z = vector1[0] * vecort2[1] - vector1[1] * vecort2[0]
    result = np.array([x, y, z])
    return result/ lg.norm(result)

def get_arrays_by_components(coords):
    X = np.array([coords[i*3] for i in range(int(len(coords)/3))])
    Y = np.array([coords[i*3 + 1] for i in range(int(len(coords)/3))])
    Z = np.array([coords[i*3 + 2] for i in range(int(len(coords)/3))])
    return X, Y, Z

def calculate_center_of_mass(charges: list, coords):
    rX, rY, rZ = get_arrays_by_components(coords)

    Xmoment_of_mass = sum(map(lambda x, y: x*MASS_CONST[y], rX, charges))
    Ymoment_of_mass = sum(map(lambda x, y: x*MASS_CONST[y], rY, charges))
    Zmonent_of_mass = sum(map(lambda x, y: x*MASS_CONST[y], rZ, charges))

    sum_of_mass = sum(map(lambda x: MASS_CONST[x], charges))

    center_of_mass = np.array([Xmoment_of_mass/sum_of_mass, Ymoment_of_mass/sum_of_mass, Zmonent_of_mass/sum_of_mass])
    print( "center mass" + str(center_of_mass))
    return center_of_mass

def shift_centor_of_coord(coords, new_centor):
    i = 0
    new_coord = np.zeros(len(coords))
    for comp in coords:
        new_coord[i] = comp - new_centor[int(i % 3)]
        i = i + 1
    return new_coord

def calculate_axis_of_inertions(charges, coords):
    rX, rY, rZ = get_arrays_by_components(coords)
    Ixx = sum(map(lambda c, y, z: MASS_CONST[c]*(y * y + z * z), charges, rY, rZ))
    Ixy = sum(map(lambda c, x, y: -MASS_CONST[c] *(x * y), charges, rX, rY))
    Ixz = sum(map(lambda c, x, z: -MASS_CONST[c] * (x * z), charges, rX, rZ))
    Iyx = sum(map(lambda c, y, x: -MASS_CONST[c] * (y * x), charges, rY, rX))
    Iyy = sum(map(lambda c, x, z: MASS_CONST[c] * (x * x + z * z), charges, rX, rZ))
    Iyz = sum(map(lambda c, y, z: -MASS_CONST[c] * (y * z), charges, rY, rZ))
    Izx = sum(map(lambda c, z, x: -MASS_CONST[c] * (z * x), charges, rZ, rX))
    Izy = sum(map(lambda c, z, y: -MASS_CONST[c] * (z * y), charges, rZ, rY))
    Izz = sum(map(lambda c, x, y: MASS_CONST[c] * (x*x + y*y), charges, rX, rY))

    Inertion = np.zeros((3, 3))
    Inertion[0,0] = Ixx
    Inertion[0,1] = Ixy
    Inertion[0,2] = Ixz
    Inertion[1,0] = Iyx
    Inertion[1,1] = Iyy
    Inertion[1,2] = Iyz
    Inertion[2,0] = Izx
    Inertion[2,1] = Izy
    Inertion[2,2] = Izz

    return Inertion


def calculate_translation_vect(charges):
    D1 = np.zeros(len(charges)*3)
    D2 = np.zeros(len(charges)*3)
    D3 = np.zeros(len(charges)*3)
    i = 0
    for charge in charges:
        D1[i*3] = math.sqrt(MASS_CONST[charge])
        D2[i*3+1] = math.sqrt(MASS_CONST[charge])
        D3[i*3+2] = math.sqrt(MASS_CONST[charge])
        i = i + 1
    D1 = D1 / np.linalg.norm(D1)
    D2 = D2 / np.linalg.norm(D2)
    D3 = D3 / np.linalg.norm(D3)

    return [D1, D2, D3]


def vector_struct_to_matrix(struct):
    return struct.reshape((-1, 3)).copy()


def internal_coords(struct, masses, charges):

    n = len(masses) * 3

    mass_center = calculate_center_of_mass(charges, struct)
    struct = shift_centor_of_coord(struct, mass_center)
    inert_axis = calculate_axis_of_inertions(charges, struct)
    eigv, X = lg.eigh(inert_axis)

    print(eigv)
    print(X)

    R = vector_struct_to_matrix(struct)
    P = R.dot(X)

    i = 0
    D = []
#    conv_mass = {1.00782505 : 1.0, 12.00000: 12.00000}

#    masses = [conv_mass[mass] for mass in masses ]
    for i in range(3):
        d = np.zeros(n)
        d[i::3] = np.sqrt(masses)
        D.append(d)

    for i in range(3):
        D.append(np.zeros(n))

    for i in range(3):
        D[3][i::3] = (P[:, 1] * X[i, 2] - P[:, 2] * X[i, 1]) * np.sqrt(masses)
        D[4][i::3] = (P[:, 2] * X[i, 0] - P[:, 0] * X[i, 2]) * np.sqrt(masses)
        D[5][i::3] = (P[:, 0] * X[i, 1] - P[:, 1] * X[i, 0]) * np.sqrt(masses)

    del_index = []
    for i in range(len(D)):
        if D[i][0] is "nan" or lg.norm(D[i]) < 1.0e-12:
            del_index.append(i)
        else:
            D[i] = D[i] / np.linalg.norm(D[i])
    if del_index:
        for i in del_index:
            del(D[i])
    return separete_basis(np.stack(D, axis=1))[:, len(D):]

