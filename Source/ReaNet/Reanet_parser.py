from Source.Utils.parser import parser
import os
class reanet_parser(parser):

    def __init__(self, file):
        super().__init__(file)

    def _get_energy(self):
        self.go_to_key("energy: ", "value:")
        value = float(self.last_line.split()[-1])
        return value

    def _get_geom(self):
        while True:
            line = next(self.iterable)
            if not "normal modes coords:" in line:
                if line.isdigit():
                    break
        number_of_atoms = line
        number_of_atoms = int(number_of_atoms)
        line = next(self.iterable)
        if "Energy:" in line or "(energy " in line:
            energy = float(line.replace(")", "").split()[-1])
        else:
            energy = None
        atoms = []
        coord = []
        for i in range(number_of_atoms):
            line = next(self.iterable)
            atoms.append(line.split()[0])
            coord.extend(map(float, line.split()[1:]))
        return atoms, coord, energy

    def _get_force(self):
        self.go_to_key("grad:")
        part_of_file = self.get_all_by_key("grad norm:")
        grads = []
        for line in part_of_file:
            list_with_deleted_symbols = []
            list_with_deleted_symbols.extend(map(lambda x : x.replace("[", "").replace("]", ""), line.split()[1:]))
            while True:
                if '' in list_with_deleted_symbols:
                    list_with_deleted_symbols.remove('')
                else:
                    break
            grads.extend(list_with_deleted_symbols)
        return grads

    @staticmethod
    def save_hessian(file, matrix):
        if os.path.isfile(file):
            os.remove(file)
        with open(file, "w") as write_file:
            accum = 0
            line = ""
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    if accum < 5:
                        line = line + "{:10.7f}".format(matrix[i, j]) + " "
                        accum = accum + 1
                    elif accum == 5:
                        line = line + "\n"
                        write_file.write(line)
                        line = ""
                        line = line + "{:10.7f}".format(matrix[i, j]) + " "
                        accum = 1
            line = line + "\n"
            write_file.write(line)

    def _get_norma_grad(self):
        self.go_to_key("grad norm:", "grad:")
        try:
            value = float(self.last_line.replace("]","").split()[-1])
        except:
            value = float(next(self.iterable).replace("]", "").split()[-1])
        return value

    def _get_delta_step(self):
        self.go_to_key("delta norm: ")
        return float(self.last_line.replace(")", "").split()[-1])

    def get_optimization_step(self):
        while True:
            try:
                charges, coords, _ = self._get_geom()
                energy = self._get_energy()
#                grads = self._get_force()
                norma_grad = self._get_norma_grad()
                delta_step = self._get_delta_step()
                yield charges, coords, energy, "None", [norma_grad, delta_step]
            except StopIteration:
                self.reset_iters()
                return

    def get_minimum_from_sub_dimentions(self):
        while True:
            try:
                charges, coords, energy = self._get_geom()
                norma_grad = 0.0
                delta_step = 0.0
                yield charges, coords, energy, "None", [norma_grad, delta_step]
            except StopIteration:
                self.reset_iters()
                return


