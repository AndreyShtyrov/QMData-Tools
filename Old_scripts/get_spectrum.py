from Source.Utils.listanalyser import ListReader
import argparse
import numpy as np


def get_spectrum(iterable, n_states):
    Es = []
    LR = ListReader(iterable)
    for i in range(n_states):
        line = LR.go_by_keys("NEVPT2 state {0} total energy:".format(i), "Total Energy (E0+dE)")
        Es.append(float(line.split()[-1]))
    return Es


def get_CAS_os(iterable, n_states, c_state):
    result = []
    LR = ListReader(iterable)
    LR.go_by_keys("* CASSCF dipole moments")
    for i in range(n_states):
        if i != c_state:
            if i > c_state:
                LR.go_by_keys("* Transition    {0} - {1} :".format(i, c_state))
            else:
                LR.go_by_keys("* Transition    {0} - {1} :".format(c_state, i))
            line = next(iterable)
            result.append(float(line.split()[-2]))
        else:
            result.append("-")
    return result


def convert_hartee_nm(sp_list, c_state):
    sp_list = sp_list - sp_list[c_state]
    for i in range(len(sp_list)):
        if sp_list[i] != 0:
            sp_list[i] = 45.5640 / sp_list[i]
        else:
            sp_list[i] = 0
    return sp_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=" it search in out file nevpt2 sp")
    parser.add_argument("n_states", type=int, help="number of roots")
    parser.add_argument("-c_state", type=int, default=0, help="root of interest")
    args = parser.parse_args()
    with open("opt.out", "r") as f:
        sp_list = np.array(get_spectrum(f, args.n_states))
        try:
            ss_list = get_CAS_os(f, args.n_states, args.c_state)
        except:
            ss_list = None
    sp_list = convert_hartee_nm(sp_list, args.c_state)
    i = 0
    with open("result.txt", "w") as f:
        for line in sp_list:
            if not ss_list:
                f.write(str(i) + " " + str(line) + "\n")
            else:
                f.write(str(i) + " " + str(ss_list[i]) + " " + str(line) + "\n")
            i += 1
