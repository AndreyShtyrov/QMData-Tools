import numpy as np
import numpy.linalg as lg
from Source.Constants.physics import CI, MASS_CONST

def read_coord():
    with open("coord.xyz", "r") as coord_file:
        n_atoms = int(next(coord_file).replace("\n", ""))
        _ = next(coord_file)
        charges = []
        coords = []
        for line in coord_file:
            charges.append(line.split()[0].upper())
            coords.extend(map(float, line.replace("\n", "").split()[1:]))
        return charges, np.array(coords) * CI.A_in_Bh

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
    rX, rY, rZ =get_arrays_by_components(coords)
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

def calcuate_inertion(charges, coords):
    mass_center = calculate_center_of_mass(charges, coords)
    new_coords = shift_centor_of_coord(coords, mass_center)
    inert_axis = calculate_axis_of_inertions(charges, new_coords)
    eigv, X = lg.eigh(inert_axis)
    return eigv, X

if __name__ == '__main__':
    charges, coords = read_coord()
    eigv, X = calcuate_inertion(charges, coords)
    print(eigv)

