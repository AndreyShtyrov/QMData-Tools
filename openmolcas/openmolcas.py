from utils.parser import parser, get_dir_tree
from openmolcas.molden import geom_file_iters
import pathlib
import shutil
import numpy as np


class open_parser(parser):
    def __init__(self, file):
        super().__init__(file)
#        message = self._check()

    @staticmethod
    def write_input_orb(orb):
        lines = []
        lines.append("#INPORB 2.2\n")
        lines.append("#INFO\n")
        lines.append("* SCF orbitals\n")
        lines.append("       0       1       2\n")
        number_mo_functions = len(orb)
        lines.append("{:>8}".format(number_mo_functions) + "\n")
        lines.append("{:>8}".format(number_mo_functions) + "\n")
        lines.append("*BC:HOST node-015 PID 23776 DATE Tue Mar 12 16:24:28 2019\n")
        lines.append("#ORB\n")
        accum = 1
        for mo in orb:
            lines.append("* ORBITAL    1" + "{:>5}".format(accum) + "\n")
            accum = accum + 1
            for i in range(round(len(mo)/5)):
                line = ""
                for element in mo[i*5:i*5 + 5]:
                    line = line + "{:>22.14E}".format(element)
                line = line + "\n"
                lines.append(line)
        return lines

    def _check_main_method(self):
        pass

    def _check(self):
        try:
            _ = self.go_to_key("&GATEWAY")
        except StopIteration:
            print("Is_not_molcas")
            exit(1)
        self.reset_iters()
        return "Ok"

    def _get_energy(self):
        pass

    def _get_force(self):
        pass

    def _get_optimization_iter(self):
        pass

def get_last_geom(path):
    geom_file = geom_file_iters(path)
    next(geom_file)
    next(geom_file)
    number_geoms = int(next(geom_file).replace("\n",""))
    for line in geom_file:
        if "[GEOMETRIES] (XYZ)" in line:
            break
    coords_number = int(next(geom_file).replace("\n",""))

    for i in range((number_geoms - 1)* (coords_number + 2)):
        _ = next(geom_file)
    _ = next(geom_file)
    result = []
    result.append(str(coords_number) +  "\n")
    result.append("\n")
    for i in range(coords_number):
        result.append(next(geom_file))
    return result

def restart_calculations():
    general_path = pathlib.Path.cwd()
    new_dir_number = 1
    for cur_dir in general_path.iterdir():
        if cur_dir.is_dir():
            if "-" in cur_dir.name:
                number = int(cur_dir.name.split("-")[0])
                if new_dir_number < number:
                    new_dir_number = number + 1
    work_dir = general_path/ (str(number) + "opt")
    work_dir.mkdir()
    coords = get_last_geom(general_path)
    input_file = ""
    for cur_file in general_path.iterdir():
        if cur_file.is_file():
            if ".inp" in cur_file.name:
                input_file = cur_file
    shutil(str(input_file), str(work_dir/"opt.inp"))
    shutil(str(general_path/"Addition_output/opt.RasOrb"), str(work_dir / "pr_orb.RasOrb"))
    with open("opt.xyz", "w") as out_geom_file:
        out_geom_file.writelines(coords)
    



