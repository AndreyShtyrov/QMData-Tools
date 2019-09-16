from Source.Constants.physics import *
from Source.Utils.listanalyser import ListReader
from Source.Common.General_Tools import *
from Source.Common.Config import config
import pathlib
import numpy as np
import json


def convert_geom(charges: np.ndarray, coords: np.ndarray):
    geom = []
    result = dict({"geometry": geom})
    for i in range(len(charges)):
        line = {"atom": CHARGES_TO_SYMBOLS[charges[i]],
                "xyz": coords[i * 3: i * 3 + 3].tolist()}
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
    part = LR.get_all_by_keys("* Projecting out translational and rotational degrees of freedom",
                              "Mass Weighted Hessian Eigenvalues")
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
    ndim = int(math.sqrt((len(temporary) - 1) * 6 + len(temporary[-1])))
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


class bagel_config(config):
    """
    :param
    method : available casscf, caspt2, nevpt2, hf
    charge : charge of system
    mult : multiplecity of system
    """
    method: int = "casscf"
    charge: int = 0
    mult: int = 1
    active: str = "2:2"
    _path_to_default_settings: pathlib.Path = pathlib.Path.home() / ".default_bagel_settings"

    def __init__(self, config: dict = dict()):
        super().__init__(config)
        self._coords = convert_geom(self._ch, self._co)

        if (pathlib.Path() / "path_to_bagel_basis").is_file():
            with open(pathlib.Path() / "path_to_bagel_basis", "r") as f:
                self.path_to_basis = str(next(f)).replace("\n", "")

    def formate_basis(self):
        if not self.path_to_basis:
            basis = self.basis
            if self.basis == "3-21g" or self.basis == "sto-3g" or self.basis == "6-31g":
                df_basis = "svp-jkfit"
            else:
                df_basis = self.basis + "-jkfit"
        else:
            basis = self.path_to_basis + self.basis + ".json"
            if self.basis == "3-21g" or self.basis == "sto-3g" or self.basis == "6-31g":
                df_basis = self.path_to_basis + "svp-jkfit.json"
            else:
                df_basis = self.path_to_basis + self.basis + "-jkfit.json"
        return basis, df_basis

    def make_make_molsp(self):
        basis, df_basis = self.formate_basis()

        molecule = {
            "title": "molecule",
            "basis": basis,
            "df_basis": df_basis,
            "angstrom": True
        }
        molecule.update(self._coords)
        return molecule

    def start_from_file(self):
        _, df_basis = self.formate_basis()
        if self.file == "molden":
            return {
                "title": "molecule",
                "basis": "molden",
                "df_basis": df_basis
            }
        elif self.file == "archive":
            return {
                "title": "load_ref",
                "file": "orb"
            }

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
                    self.n_act = int(value.split(":")[0])
                    self.n_el = int(value.split(":")[1])
                if "charge" in key:
                    self.charge = int(value)
                    self.mult = int(((self.n_el - self.charge) % 2) + 1)
                if "mult" in key:
                    self.mult = int(value)
                if "n_state" in key:
                    self.n_state = int(value)
                if "target" in key:
                    value = value
                    self.target = int(value)
                if "save" in key:
                    self.save = bool(value)
                if "load" in key:
                    self.load = bool(value)
                if "type_job" in key:
                    self.type_job = str(value).lower()
                if "method" in key:
                    self.method = str(value).lower()
                if "basis" in key:
                    self.basis = str(value).lower()
                if "path_to_bagel_basis" in "key":
                    self.basis = str(value).lower()
                if "alert" in key:
                    self.alert = [int(i) for i in value]
                if "file" in key:
                    self.file = str(value).lower()

    def convert_file_in_dict(self, file_name) -> dict:
        result = dict()
        with open(file_name, "r") as f:
            for line in f:
                if line.split("=")[0].replace(" ", "") == "alert":
                    result.update({line.split("=")[0]: line.split("=")[-1].replace("\n", "").replace(" ", "").split()})
                else:
                    result.update({line.split("=")[0]: line.split("=")[-1].replace("\n", "").replace(" ", "")})

        return result

    def make_casscf_molsp(self):
        if self.alert:
            self.save = True
            return {
                "title": "casscf",
                "charge": self.charge,
                "nact": self.n_act,
                "active": self.alert,
                "fci_algorithm": "knowles",
                "nclosed": int(self.n_orb - (self.n_el // 2) - (self.charge // 2)),
                "nstate": self.n_state
            }
        return {
            "title": "casscf",
            "charge": self.charge,
            "nact": self.n_act,
            "fci_algorithm": "knowles",
            "nclosed": int(self.n_orb - (self.n_el // 2) - (self.charge // 2)),
            "nstate": self.n_state
        }

    def make_caspt_molsp(self):
        return {
            "title": "smith",
            "method": "caspt2",
            "ms": True,
            "xms": True,
            "sssr": True
        }

    def make_nevpt2_molsp(self):
        result = []
        for i in range(self.n_state):
            temp = {
                "title": self.method,
                "charge": self.charge,
                "nact": self.n_act,
                "nclosed": int(self.n_orb - (self.n_el // 2) - (self.charge // 2)),
                "nstate": self.n_state,
                "maxiter": 80,
                "thresh": 1.0e-6,
                "thresh_scf": 1.0e-6,
                "thresh_fci": 1.0e-7,
                "istate": i
            }
            result.append(temp)
        return result

    def make_scf(self):
        method = "uhf"
        if self.mult is 1:
            method = "hf"
        return {
            "title": method,
            "charge": self.charge,
            "nopen": int(self.mult - 1)
        }

    def make_opt_mosp(self, method):
        if self.method == "opt_ts":
            return {
                "title": "optimize",
                "opttype": "transition",
                "target": self.target,
                "method": method,
                "hess_approx": False
            }
        elif self.method == "minimal":
            return {
                "title": "optimize",
                "opttype": "energy",
                "target": self.target,
                "method": method
            }
        elif self.method == "conical":
            return {
                "title": "conical",
                "opttype": "energy",
                "target": self.target,
                "target2": self.target + 1,
                "method": method
            }
        print("unknowen type_job specified")
        exit(2)

    def make_grads_mosp(self, method):
        return {
            "title": "force",
            "dipole": True,
            "target": self.target,
            "method": [method]
        }

    def make_input_body(self):
        inp_file = {"bagel": []}
        if self.file:
            inp_file["bagel"].append(self.start_from_file())
        else:
            inp_file["bagel"].append(self.make_make_molsp())
        if pathlib.Path("orb.archive").is_file():
            inp_file["bagel"].append(self.read_orb())

        calc = None
        if self.method == "casscf":
            calc = self.make_casscf_molsp()
        elif self.method == "caspt2":
            inp_file["bagel"].append(self.make_casscf_molsp())
            calc = self.make_caspt_molsp()
        elif self.method == "nevpt2":
            inp_file["bagel"].append(self.make_casscf_molsp())
            calc = self.make_nevpt2_molsp()
            inp_file["bagel"].extend(calc)
            calc = self.make_casscf_molsp()
        elif self.method == "hf":
            calc = self.make_scf()

        if not calc:
            print("Undefine method")
            exit(2)

        if self.type_job == "force":
            calc = self.make_grads_mosp(calc)
        elif self.type_job == "energy":
            pass
        else:
            self.make_opt_mosp(self.method)

        inp_file["bagel"].append(calc)




        if self.save is True:
            inp_file["bagel"].append(self.save_orb())
            inp_file["bagel"].append(self.save_molden())
        self.save_json(inp_file, "opt.json")
        self.save_values_in_template(pathlib.Path("pr_template"))
        self.show_job_specification()

    @staticmethod
    def get_geom_from_bagel_input(file):
        data = json.load(open(file, "r"))
        geom = data["bagel"]["molecule"]["geometry"]
        charges = [SYMBOLS_TO_CHARGES[i["atom"]] for i in geom]
        coords = []
        coords.extend([i["xyz"] for i in geom])
        return charges, np.array(coords)

    def save_json(self, data: dict, file_name: str):
        with open(file_name, "w") as f:
            f.writelines(json.dumps(data, indent=2))


if __name__ == '__main__':
    bg = bagel_config()
    get_hessian([])
#    ch, coor = bagel_config.get_geom_from_bagel_input("opt.json")

#    with open("coord.xyz", "w") as f:
#        save_geom_xyz(ch, coor)
