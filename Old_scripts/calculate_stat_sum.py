import numpy
import sys
import math
from Source.Constants.physics import *
from Source.Utils.molecul_property import read_coord, calcuate_inertion

def read_freqs(file_name = "freq.txt"):
    result = []
    with open(file_name, "r") as freqs_file:
        for line in freqs_file:
            result.append(float(line.replace("\n", "")))
    return result

def calculate_Ezero_correction(freqs):
    result = 0
    for freq in freqs:
        result = result + CI.h * CI.convert_energy("cm-1", "hz", freq) / 2
    return result * CI.Na

def calculate_Spost(charges, T):
    mass_sum = sum(map(lambda x : CI.convert_energy("a.e.m", "kg", MASS_CONST[x]), charges))
    result = (2 * math.pi * mass_sum * CI.Kb * T) ** (3/2) * CI.R * T
    result = result / (CI.h ** 3 * CI.Na * CI.Pa)
    result = CI.R * math.log(result, math.e) + 5/2 * CI.R
    return result

def calculate_B(eig):
    result = CI.h / (8 * (math.pi ** 2) * CI.light_speed)
    result = result / CI.convert_energy("a.u.m*br^2", "kg*m^2", eig)
    return result


def calculate_Srot(T, eigv_inertion, sigma=1):
    result = 1
    is_line_mol = True
    for i in eigv_inertion:
        _value = (CI.Kb * T / (calculate_B(i) * CI.h * CI.light_speed)) ** 0.5
        if _value == 0:
            is_line_mol = True
        else:
            result = result * _value
    if not is_line_mol is True:
        result = result * (math.pi ** 0.5 ) / sigma
        result = CI.R * math.log(result, math.e) + 1.5 * CI.R
    else:
        result = result / sigma
        result = CI.R * math.log(result, math.e) + CI.R
    return result


def calculate_TdQdT(freqs, T):
    result = 0
    for freq in freqs:
        exp_value = CI.h * CI.light_speed * freq * 100/ (CI.Kb * T)
        result = result + exp_value / (math.e ** (exp_value) - 1)
    return result

def calculate_TdQdTH(freqs, T):
    result = 0
    for freq in freqs:
        exp_value = CI.h * CI.light_speed * freq * 100 / (CI.Kb * T)
        result = result + exp_value / (math.e ** (exp_value) - 1)
    return result

def calculate_Q(freqs, T):
    result = 1
    for freq in freqs:
        exp_value = CI.h * CI.light_speed * freq * 100/ (CI.Kb * T)
        result = result * 1 / (1 - math.e ** (- exp_value))
    return result


def calculate_Svib(freqs, T):
    result = CI.R * math.log(calculate_Q(freqs, T), math.e)
    result = result + CI.R * calculate_TdQdT(freqs, T)
    return result


def calculate_H_correction(freqs, T, is_line_mol):
    result = CI.R * T * calculate_TdQdTH(freqs, T)
    if is_line_mol:
        result = (7/2 + 1) * CI.R * T + result
    else:
        result = 4 * CI.R * T + result
    result = calculate_Ezero_correction(freqs) + result
    return result

def delete_negative_freqs(freqs):
    result = []
    for freq in freqs:
        if freq > 0:
            result.append(freq)
    return result

def calc_g(charges, eignv, freqs, coeff, T):
    freqs1 = freqs * coeff
    S = 0
    S = calculate_Spost(charges, T) + S
    S = calculate_Srot(T, eignv, 1) + S
    S = calculate_Svib(freqs1, T) + S
    H = calculate_H_correction(freqs1, T, False)
    G = H - S * T
    return G

if __name__ == '__main__':
#    print(calculate_Spost(["O", "O", "H", "H", ], 298.15) * 0.239006)
#    print(calculate_B(15.34965))
#    print(calculate_Srot(298.15, [6.18677, 67.22231, 69.99067], 1) * 0.239006)

#    print(calculate_Srot(298.15, [7.67483, 7.67483, 15.34965] ))
#    freqs = [ 1260.9017,  1450.7553, 1640.8516,  4520.4600, 4531.8614]

#    freqs = delete_negative_freqs(freqs)
#    print(calculate_Svib(freqs, 298.15) * 0.239006)
#    print(calculate_Ezero_correction(freqs)/2625.5/1000)
#    print(calculate_Svib(freqs, 298.15) * 0.239006)
#    print(calculate_H_correction(freqs, 298.15, False)/2625.5/1000)
    freqs = read_freqs("freq.txt")
    charges, coords = read_coord()
    charges = [CHARGES_TO_SYMBOLS[i] for i in charges]
    eignv, _ = calcuate_inertion(charges, coords)
    freqs = delete_negative_freqs(freqs)
    T = 298.15
    # try:
    #     coeff = float(sys.argv[1])
    # except:
    #     coeff = 1
    # coeff = 0.90
    coeff = 1
    freqs = numpy.array(freqs)
    print("H " + str(calculate_H_correction(freqs, 298.15, False)/2625.5/1000))
    print(calc_g(charges, eignv, freqs, coeff, T) /2625.5/1000)
