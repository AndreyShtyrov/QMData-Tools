import pathlib
import yaml


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

    def load_values_from_template(self, config: dict):
        parent_class = type(self)
        for attr in config.keys():
            if attr in parent_class.__annotations__.keys():
                if isinstance(config[attr], list):
                    setattr(self, [ int(i) for i in config[attr]])
                else:
                    setattr(self, attr, config[attr])
                    
    def save_values_in_template(self, path: pathlib.Path):
        result = dict()
        parent_class = type(self)
        for attr in parent_class.__annotations__.keys():
            result.update({attr: getattr(self, attr)})
        self.save_file(path, result)
        

    def load_file(self, path):
        with open(path, "r") as steam:
            file = yaml.load(steam)
        return file

    def save_file(self, path: pathlib.Path, config):
        path.write_text(yaml.dump(config, indent=2))

    def make_table_all_avaliable_classes(self):
       pass


if __name__ == '__main__':
    conf = config()



