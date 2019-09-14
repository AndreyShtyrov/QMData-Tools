from Source.Gaussian09.Gaussian09 import g09_parser
from Source.Utils.listanalyser import ListReader


class parser(object):

    def __init__(self, file_name):
        self.parser = g09_parser
        self.file_name = file_name
        self.check_term(self.file_name)
        with open(self.file_name, "r") as open_file:
            self.parser = self.parser(open_file)


    def check_term(self, file_name):
        pass

    def get_optimizations_steps(self):
        result = {}
        i = 0
        for opt_iter in self._get_opt_iterations():
            result.update({
                i : {
                    "energy" : opt_iter[0],
                    "charges": opt_iter[1],
                    "coords": opt_iter[2],
                    "forces": opt_iter[3],
                    "crit": opt_iter[4],
                    "eing": opt_iter[5]

                }
            })
            return result

    def get_optimization_geometry(self):
        last_iter = None
        for opt_iter in self._get_opt_iterations():
            last_iter = opt_iter
        if last_iter:
            result = {"charges": last_iter[1],
                      "coords": last_iter[2]}
        else:
            with open(self.file_name, "r") as open_file:
                last_iter = self.parser.get_coord(open_file)
                result = {"charges": last_iter[0],
                          "coords": last_iter[1]}
        return result

    def get_energy(self):
        last_iter = None
        for opt_iter in self._get_opt_iterations():
            last_iter = opt_iter
        if last_iter:
            result = last_iter[0]
        else:
            with open(self.file_name, "r") as open_file:
                result = self.parser.get_energy(open_file)
        return result

    def _get_alone_value(self, name):
        pass

    def _get_opt_iterations(self):
        stop_key = self.parser.get_stop_key("opt_cycl")
        with open(self.file_name, "r") as open_file:
            LR = ListReader(open_file)
            if "pre_key" in stop_key.keys():
                LR.go_by_keys(*stop_key["pre_key"])
            part = []
            part.extend(LR.get_all_by_end_and_keys(*stop_key["start"]))
            part.extend(LR.get_all_by_end_and_keys(*stop_key["end"]))
            while part is not []:
                energy = self.parser.get_energy(part)
                charges, coords = self.parser.get_coord(part)
                forces = self.parser.get_force(part)
                criteries = self.parser.get_criteria(part)
                eing = self.parser.get_criteria(part)
                yield energy, charges, coords, forces, criteries, eing
                part = []
                part.extend(LR.get_all_by_end_and_keys(*stop_key["start"]))
                part.extend(LR.get_all_by_end_and_keys(*stop_key["end"]))


if __name__ == '__main__':
    p = parser("opt.out")
    optimization = p.get_optimization_geometry()
    print(optimization)