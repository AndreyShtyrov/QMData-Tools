import math

MASS_CONST = {"H": 1.00782505, "C" : 12.00000, "B":  11.00931, "N": 14.00, "CL": 34.96885, "O": 15.99491}
CHARGES_TO_SYMBOLS = {1: "H",
                      2: "He",
                      3: "Li",
                      6: "C",
                      7: "N",
                      8: "O",
                      9: "F",
                      17: "Cl",
                      16: "Si",
                      15: "P",
                      29: "Cu",
                      26: "Fe"}

SYMBOLS_TO_CHARGES = {
    "H": 1,
    "C": 6,
    "O": 8,
    "N": 7
}

class CI():
    Kb = 1.38064852e-23
    R = 8.31446
    Na = 6.02214129e23
    cJinh = 2625500
    h = 6.62607004e-34
    light_speed = 299792458
    Pa = 101325
    A_in_Bh = 1.889725989

    @classmethod
    def convert_energy(cls, first, second, value):
        if first == "cm-1":
            if second == "j/mol":
                return value * 1.196265E-2 * 1000
            elif second == "hartree":
                return value * 4.556335E-6
            elif second == "hz":
                return value * cls.light_speed * 100
        elif first == "a.e.m":
            if second == "kg":
                return value * 1.6605388e-27
        elif first == "a.u.m*br^2":
            if second == "kg*m^2":
                return value * 1.6605388e-27 * (5.2917e-11 ** 2)
        pass

class AU():

    light_spead = 123