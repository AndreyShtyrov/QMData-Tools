from Constants.physics import *
from common.QM_parser import ListReader
from common.utils import *
import pathlib
import numpy as np
import json
from types import ModuleType


def convert_geom(charges: np.ndarray, coords: np.ndarray):
    geom = []
    result = dict({"geometry": geom})
    for i in range(len(charges)):
        line = {"atom": CHARGES_TO_SYMBOLS[charges[i]],
                "xyz": coords[i*3: i*3 + 3].tolist()}
        result["geometry"].append(line)
    return result


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


class bagel_config():
    """
    :param
    method : available casscf, caspt2, nevpt2, hf
    charge : charge of system
    mult : multiplecity of system
    """
    method = "casscf"
    charge = 0
    mult = 1

    def __init__(self, config: dict):
        coord_file = pathlib.Path("coord.xyz")
        assert coord_file.is_file()

        ch, co = read_xyz(coord_file)
        self._coords = convert_geom(ch, co)
        n_el = sum(ch)
        self.n_orb = n_el // 2
        self.mult = (n_el % 2) + 1
        self.n_el = 2
        self.n_act = 2
        self.n_state = 2
        self.target = 1
        self.load = True
        self.save = False

        if pathlib.Path("template").is_file():
            config_from_file = self.convert_file_in_dict((pathlib.Path("template")))
            self.load_value_from_template(config_from_file)
        self.load_value_from_template(config)

    def make_make_molsp(self):
        inp_file = dict()
        molecule = {
            "title": "molecule",
            "basis": "3-21g",
            "df_basis": "svp-jkfit",
            "angstrom": True
        }
        molecule.update(self._coords)
        return molecule

    def read_orb(self):
        return {
            "title": "load_ref",
            "file": "orb",
            "continue_geom": False
        }

    def save_orb(self):
        return {
            "title": "save_ref",
            "file": "orb"
        }

    def save_molden(self):
        return {
            "title": "print",
            "file": "orbitals.molden",
            "orbitals": True
        }

    def load_value_from_template(self, config: dict):
        if bool(config):
            for key, value in config.items():
                if "active" in key:
                    value = value.replace("\n", "").replace(" ", "")
                    self.n_act = int(value.split(":")[0])
                    self.n_el = int(value.split(":")[1])
                if "charge" in key:
                    value = value.replace("\n", "").replace(" ", "")
                    self.charge = int(value)
                    self.mult = int(((self.n_el - self.charge) % 2) + 1)
                if "mult" in key:
                    value = value.replace("\n", "").replace(" ", "")
                    self.mult = int(value)
                if "nstate" in key:
                    value.replace("\n", "").replace(" ", "")
                    self.n_state = int(value)
                if "target" in key:
                    value = value.replace("\n", "").replace(" ", "")
                    self.target = int(value)
                if "save" in key:
                    self.save = bool(value.replace("\n", "").replace(" ", ""))
                if "load" in key:
                    self.load = bool(value.replace("\n", "").replace(" ", ""))

    def convert_file_in_dict(self, file_name)-> dict:
        result = dict()
        with open(file_name, "r") as f:
            for line in f:
                result.update({line.split("=")[0], line.split("=")[-1]})
        return result

    def make_calculations_molsp(self):
        method = {
            "title": self.method,
            "charge": self.charge,
            "nact": self.n_act,
            "nclosed": int(self.n_orb - (self.n_el //2) - (self.charge // 2)),
            "nstate": self.n_state
        }

        calc = {
            "title": "force",
            "dipole": True,
            "target": self.target,
            "method": [method]
        }

        inp_file = {"bagel": []}
        inp_file["bagel"].append(self.make_make_molsp())
        if pathlib.Path("orb.archive").is_file():
            inp_file["bagel"].append(self.read_orb())
        inp_file["bagel"].append(calc)
        if self.save is True:
            inp_file["bagel"].append(self.save_orb())
            inp_file["bagel"].append(self.save_molden())
        self.save_json(inp_file, "opt.json")

    @staticmethod
    def get_geom_from_bagel_input(file):
        data = json.load(open(file, "r"))
        geom = data["bagel"]["molecule"]["geometry"]
        charges = [ SYMBOLS_TO_CHARGES[i["atom"]] for i in geom]
        coords = []
        coords.extend([i["xyz"] for i in geom])
        return charges, np.array(coords)

    def save_json(self, data: dict, file_name: str):
        with open(file_name, "w") as f:
            f.writelines(json.dumps(data, indent=2))


if __name__ == '__main__':
    ch, coor = bagel_config.get_geom_from_bagel_input("opt.json")
    with open("coord.xyz", "w") as f:
        save_geom_xyz(ch, coor)

