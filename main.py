from gaussian09.gaussian09 import g09_parser
import sys, os
from termcolor import colored, cprint

if __name__ == '__main__':
    calc = g09_parser(sys.argv[1])

    if sys.argv[2] == 'make_geom':
        generator_get_opt_inter = calc.get_optimazed_geom()
        acc = 0
        while True:
            try:
                charg, coord = next(generator_get_opt_inter)
                os.mkdir("step_" + str(acc))
                with open("step_" + str(acc) + "/coord.xyz", "w") as write_file:
                    iter_charge = iter(charg)
                    iter_coord = iter(coord)
                    for ch in iter_charge:
                        line = str(ch) + "  " + str(next(iter_coord)) + " " + str(next(iter_coord)) + " " + str(next(iter_coord))
                        write_file.write(line + "\n")
                    acc = acc + 1
            except StopIteration:
                print("End_of_Opt")
                break