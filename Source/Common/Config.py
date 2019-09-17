import pathlib
import yaml

from Source.Common.General_Tools import *


class config():
    alert: list = None
    mult: int = 1
    n_act: int = 2
    n_el: int = 2
    file: str = None
    n_state: int = 1
    target: int = 0
    load: bool = True
    save: bool = False
    path_to_basis: str = None
    basis: str = "sto-3g"
    method: str = "hf"
    type_job: str = "energy"
    _path_to_default_settings: pathlib.Path = pathlib.Path.home()/".default_settings"

    def __init__(self, config=dict()):
        coord_file = pathlib.Path("coord.xyz")
        assert coord_file.is_file()

        self._ch, self._co = read_xyz(coord_file)

        n_el = sum(self._ch)
        self.alert = None
        self.n_orb = int(n_el // 2)
        self.mult = int((n_el % 2) + 1)
        self.n_el = 2
        self.n_act = 2
        self.file = None
        self.n_state = 2
        self.target = 1
        self.load = True
        self.save = False
        self.path_to_basis = None
        self.basis = "3-21g"
        self.method = "casscf"
        self.type_job = "force"

        if self._path_to_default_settings.is_file():
            config_from_file = self.convert_file_in_dict(self._path_to_default_settings)
            self.load_values_from_template(config_from_file)

        if pathlib.Path("template").is_file():
            config_from_file = self.load_file((pathlib.Path("template")))
            self.load_values_from_template(config_from_file)
        self.load_values_from_template(config)

    def show_job_specification(self):
        print("")
        print("++++++++++++++++++++++++++++++++++++")
        print("+ method : {:>23} +".format(self.method))
        if hasattr(self, "charge"):
            print("+ charge : {:>23} +".format(self.charge))
        print("+ basis : {:>24} +".format(self.basis))
        if hasattr(self, "active"):
            print("+ active : {:>23} +".format(self.active))
        print("+ mult : {:>25} +".format(self.mult))
        print("+ n_state : {:>22} +".format(self.n_state))
        print("++++++++++++++++++++++++++++++++++++")


    def load_values_from_template(self, config: dict):
        for attr in config.keys():
            if attr in self._get_all_default_fields().keys():
                if attr == "active":
                    setattr(self, attr, config[attr])
                    self.n_el = int(config[attr].split(":")[0])
                    self.n_act = int(config[attr].split(":")[1])
                if isinstance(config[attr], list):
                    setattr(self, [ int(i) for i in config[attr]])
                else:
                    setattr(self, attr, config[attr])

    def _get_all_default_fields(self) -> dict:
        parent_class = type(self)
        all_properties = parent_class.__annotations__
        all_properties.update(type(self).__bases__[0].__annotations__)
        return all_properties

    def save_values_in_template(self, path: pathlib.Path):
        result = dict()
        for attr in self._get_all_default_fields().keys():
            if type(getattr(self, attr)) is pathlib.Path:
                result.update({attr: str(getattr(self, attr))})
            else:
                result.update({attr: getattr(self, attr)})
        self.save_file(path, result)
        

    def load_file(self, path):
        with open(path, "r") as steam:
            file = yaml.load(steam)
        return file

    def save_file(self, path: pathlib.Path, config):
        data = yaml.dump(config, indent=2, default_flow_style=False)
        path.write_text(data)

    def make_table_all_avaliable_classes(self):
       pass


    def make_input_body(self):
        pass


if __name__ == '__main__':
    conf = config()

