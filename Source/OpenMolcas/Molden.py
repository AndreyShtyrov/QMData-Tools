from Source.Utils.parser import parser, get_dir_tree
import pathlib

Name_Space_molden_read_function = []

class molden_parser(parser):
    def __init__(self, file):
        super().__init__(file)
#        message = self._check()

    def get_mo(self):
        return self._get_mo()

    def _get_mo(self):
        result = []
        self.go_to_key("[MO]")
        self.go_to_key("Occup=")
        trigger = True
        while trigger:
            try:
                mo_lines = self.get_all_by_keys_and_endfile("Sym=")
                self.go_to_key("Occup=")
            except StopIteration:
                trigger = False
            mo = []
            mo.extend(map(lambda x: float(x.split()[1]), mo_lines))
            result.append(mo)
        return result

    @staticmethod
    def write_optimization_molden(list_of_energy, list_of_tuple_charge_coords, list_of_grads, list_of_criteries):
        list_lines = []
        list_lines.append(" [MOLDEN FORMAT]\n")
        list_lines.append(" [N_GEO]\n")
        number_of_atoms = len(list_of_tuple_charge_coords[0])
        list_lines.append("{:>22}".format(number_of_atoms) + "\n")
        list_lines.append(" [GEOCONV]\n")
        list_lines.append(" energy\n")
        for energy in list_of_energy:
            list_lines.append("{:>24.17E}".format(energy) + "\n")
        list_lines.append(" max-force\n")
        for force_delta in list_of_criteries:
            list_lines.append("{:>12.7}".format(force_delta[0])+ "\n")
        list_lines.append(" rms-force\n")
        for force_delta in list_of_criteries:
            list_lines.append("{:>12.7}".format(force_delta[1]) + "\n")
        list_lines.append(" [GEOMETRIES] (XYZ)\n")
        for i in range(len(list_of_energy)):
            list_lines.append("{:>4}".format(number_of_atoms)+ "\n")
            list_lines.append("{:>19.15f}".format(list_of_energy[i])+ "\n")
            for tuple_charge_coords in list_of_tuple_charge_coords[i]:
                line = " " + tuple_charge_coords["charges"]
                line = line + "{:>15.7f}".format(tuple_charge_coords["coords"][0])
                line = line + "{:>15.7f}".format(tuple_charge_coords["coords"][1])
                line = line + "{:>15.7f}".format(tuple_charge_coords["coords"][2])
                list_lines.append(line + "\n")
        list_lines.append(" [FORCES]\n")
        i = 1
        for force in list_of_grads:
            list_lines.append("point" + "{:>5}".format(i)+ "\n")
            i = i + 1
            for line_of_force in force:
                line = "{:>15.7}".format(line_of_force[0])
                line = line + "{:>15.7}".format(line_of_force[1])
                line = line + "{:>15.7}".format(line_of_force[2])
                list_lines.append(line + "\n")
        return list_lines


    def _check_main_method(self):
        pass

    def _check(self):
        try:
            _ = self.go_to_key("[MOLDEN FORMAT]")
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
    
def get_first_geom(path) -> pathlib.Path:
    for cur_file in get_dir_tree(path):
        if "geo.molden" in cur_file.name:
            return  cur_file

def geom_file_iters(path: pathlib.Path) -> iter:
    molden_geom_file = get_first_geom(path)
    with open(molden_geom_file, "r") as molden_geom_file:
        for line in  molden_geom_file:
            yield line
    return
    

