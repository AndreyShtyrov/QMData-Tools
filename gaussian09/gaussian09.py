from utils.listanalyser import ListAnalyser, get_first_number, ListReader
import numpy as np



class g09_parser(ListAnalyser):
    stop_keys = {"Opt_cylc_start": {"Berny optimization."},
                      "Opt_cylc_end": {"GradGradGradGradGradGradGrad"},
                      "method": {"#"},
                      "opt_geom_start": {"Input orientation:", "Standard orientation:", "Z-Matrix orientation:"},
                      "opt_geom_end": {"----------------------------------------------"},
                      "force_start": {"Forces (Hartrees/Bohr)"},
                      "force_end": {"-------------------------------------------------------------------"},
                      "crit_start": {"Item               Value"},
                      "crit_end": {"Predicted change"},
                      "EigV_opt": {"Eigenvalues ---"},
                      "pop_start": {"Population analysis using the SCF density."},
                      "pop_end": {"Alpha  occ. eigenvalues --", "Alpha virt. eigenvalues --"},
                      "opt_cycl": {"start": {"Berny optimization."},
                                   "pre_key": {"Initialization pass."},
                                   "end": {"GradGradGradGradGradGradGrad"}}
                      }

    def __init__(self, lines):
        super().__init__()
        self.main_method = None
        self.nroots = 1
        self.pt2 = False
        self.root = 0
        self.emperic = False
        self.casscf = False
        self.define_methods(lines)

    @classmethod
    def get_stop_key(cls, name):
        return cls.stop_keys[name]

    def get_energy(self, lines):
        LR = ListReader(lines)
        if self.casscf:
            pass
        elif self.nroots is not 1 and not self.casscf:
            pass
        elif self.emperic:
            line = self._go_by_keys(lines, "Energy=")
            return float(line.split()[1].replace("D", "E"))
        elif self.nroots is 1 and not self.pt2:
            line = LR.go_by_keys("SCF Done:")
            return float(line.split()[4])
        elif self.nroots is 1 and self.pt2:
            line = LR.go_by_keys("E(PMP2)=", "E2(B2PLYPD)")
            return float(line.split()[-1].replace("D", "E"))

    def define_methods(self, lines):
        line = self._go_by_keys(lines, *self.stop_keys["method"])
        if "CASSCF" in line.upper():
            self.casscf = True
            if "NROOT" in line.upper():
                sh_line = line.upper().split("NROOT")[-1]
                sh_line = sh_line.split(")")[0]
                self.nroots = get_first_number(sh_line)
                self.root = self.nroots
        elif "PT2" in line.upper() or "PL" in line.upper():
            self.pt2 = True
        elif "TD" in line:
            self.nroots = 3
            self.root = 0
            if "NSTATES" in line.upper():
                sh_line = line.upper().split("NSTATES")[-1]
                self.nroots = get_first_number(sh_line)
            if "ROOT" in line.upper():
                sh_line = line.upper().split("ROOT")[-1]
                self.root = get_first_number(sh_line)
        elif "MINDO3" in line:
            self.emperic = True

    def get_force(self, lines) -> np.ndarray:
        LR = ListReader(lines)
        LR.go_by_keys(*self.stop_keys["force_start"])
        LR.get_next_lines(2)
        part = LR.get_all_by_keys(*self.stop_keys["force_end"])
        result = []
        for line in part:
            result.extend(map(float, line.replace("\n" , "").split()[2:]))
        return np.array(result)

    def get_coord(self, lines) -> tuple:
        LR = ListReader(lines)
        LR.go_by_keys(*self.stop_keys["opt_geom_start"])
        LR.go_by_keys("--------------------------")
        LR.get_next_lines(3)
        part = LR.get_all_by_keys(*self.stop_keys["opt_geom_end"])
        charges = []
        coords = []
        for line in part:
            charges.append(line.split()[1])
            coords.extend(map(float, line.replace("\n", "").split()[3:]))
        return charges, np.array(coords)

    def get_criteria(self, lines) -> dict:
        result = dict()
        LR = ListReader(lines)
        LR.go_by_keys(*self.stop_keys["crit_start"])
        part = LR.get_all_by_keys(*self.stop_keys["crit_end"])
        try:
            for line in part:
                result.update({line.split()[0] + " " + line.split()[1]: line.split()[2]})
            return result
        except:
            return np.nan

    def get_EigV_optimization(self, lines) -> np.ndarray:
        part = []
        result = []
        LR = ListReader(lines)
        line = LR.go_by_keys(*self.stop_keys["EigV_opt"])
        result.extend(map(float, line.replace("\n", "").split()[2:]))
        part.append(line)
        part = LR.get_all_if_keys(*self.stop_keys["EigV_opt"])
        for line in part:
            result.extend(map(float, line.replace("\n", "").split()[2:]))
        return np.array(result)

    def get_MO(self, lines):
        LR = ListReader(lines)
        line = LR.go_by_keys(*self.stop_keys["pop_end"])
        coeff = []
        coeff.extend(map(float, line.replace("\n", "").split()[4:]))
        part = LR.get_all_if_keys(*self.stop_keys["pop_end"])
        for line in part:
            coeff.extend(map(float, line.replace("\n", "").split()[4:]))
        n_basis = len(coeff)
        MO = np.zeros((n_basis, n_basis))
        LR.get_next_lines(3)
        for i in range(int(n_basis/5)):
            part = LR.get_all_by_keys("Eigenvalues --")
            part = iter(part)
            j = 0
            for line in part:
                if j == n_basis:
                    break
                if len(line.split()) == 5:
                    break
                elif len(line.split()) == 9:
                    MO[i * 5: i * 5 + 5, j] = line.replace("\n", "").split()[4:]
                else:
                    MO[i * 5: i * 5 + 5, j] = line.replace("\n", "").split()[2:]
                j = j + 1
        last_orb = n_basis % 5
        part = LR.get_all_by_keys("orbital", "pop", "Density Matrix:")
        j = 0
        i = int(n_basis/5)
        res = n_basis % 5
        if res is not 0:
            for line in part:
                if len(line.split()) == last_orb + 4:
                    MO[i * 5: i * 5 + res, j] = line.replace("\n", "").split()[4:]
                else:
                    MO[i * 5: i * 5 + res, j] = line.replace("\n", "").split()[2:]
                j = j + 1
        for i in range(MO.shape[0]):
            for j in range(MO.shape[1]):
                MO[i, j] = float(MO[i, j])
        return coeff, MO

    def get_hessian(self, lines):
        LR = ListReader(lines)
        LR.go_by_keys("The second derivative matrix:")
        LR.get_next_lines(1)
        part = LR.get_all_by_keys("ITU=  0")
        part1 = iter(part)
        n = 0
        for i in part1:
            try:
                _ = float(i.split()[1])
            except:
                break
            n = n + 1
        part = iter(part)
        hessian = np.zeros((n, n))
        i = 0
        shifts = int(n / 5)
        if n % 5 != 0:
            shifts = shifts + 1
        for j in range(shifts):
            for i in range(n - j*5):
                try:
                    line = next(part)
                    line = line.replace("\n", "")
                    l = i + 1
                    if l > 5:
                        l = 5
                    hessian[i + j*5, j*5: j*5 + l] = [x for x in map(float, line.split()[1:])]
                except StopIteration:
                    break
            try:
                next(part)
            except StopIteration:
                break
        for i in range(n):
            for j in range(i):
                hessian[j, i] = hessian[i, j]
        return hessian

    def get_berny_section(self, iterable):
        LR = ListReader(iterable)
        LR.go_by_keys(self.stop_keys["opt_cycle"]["start"])
        LR.go_by_keys(self.stop_keys["opt_cycle"]["start"])
        part = []
        part = LR.get_all_by_end_and_keys(self.stop_keys["opt_cycle"]["start"])
        part.extend(LR.get_all_by_end_and_keys(self.stop_keys["opt_cycle"]["start"]))
        while not part is []:
            yield part
            temp = LR.get_all_by_end_and_keys(self.stop_keys["opt_cycle"]["start"])
            part = temp
            temp = LR.get_all_by_end_and_keys(self.stop_keys["opt_cycle"]["start"])
            try:
                part.extend(temp)
            except:
                if part is not[]:
                    yield part
                break
        return

    def get_last_geom(self, iterable):
        berny_sections = get_first_number(iterable)
        for i in berny_sections:
            charge, coords = self.get_geom(i)
        return charge, coords

    def get_optimization_step(self, iterable):
        berny_sections = get_first_number(iterable)
        for i in berny_sections:
            energy = self.get_energy(i)
            grads = self.get_force(i)
            charge, coords = self.get_geom(i)
            criteria = self.get_criteria(i)
            EigV = self.get_EigV_optimization(i)
            yield charge, coords, energy, grads, criteria, EigV

    def get_optimazed_geom(self):
        for part_of_file in self._get_berny_section():
            iterable = iter(part_of_file)
            if self._is_key_in_list(iterable, "Optimization completed."):
                iterable = iter(part_of_file)
                charges, coord = self._get_geom(iterable)
                yield charges, coord
        return

    def get_optimizaition_iteration(self):
        try:
            for part_of_file in self._get_berny_section():
                line_iterator = iter(part_of_file)
                charge, geom = self._get_geom(line_iterator)
                energy = self._get_energy(line_iterator)
                force = self._get_force(line_iterator)
                eing = self._get_first_eigen(line_iterator)
                line_iterator = iter(part_of_file)
                pr_eing = self._get_first_eigen_projection(line_iterator)
                crit = self._get_criterion(line_iterator)
                yield charge, geom, energy, force, eing, crit, pr_eing
        except StopIteration:
            return
    @staticmethod
    def write_input_orb(orb):
        lines = ["(3E20.8)\n"]
        num = 1
        for mo in orb:
            lines.append(str(num) + "\n")
            trigger = 0
            string = ""
            num = num + 1
            for coeff in mo:
                if trigger == 0:
                    string = ""
                if trigger < 2:
                    if not coeff < 0:
                        string = string + "    {:=13.10E}".format(coeff)
                    else:
                        string = string + "   {:=14.10E}".format(coeff)
                    trigger = trigger + 1
                else:
                    trigger = 0
                    if not coeff < 0:
                        string = string + "    {:=13.10E}".format(coeff)
                    else:
                        string = string + "   {:=14.10E}".format(coeff)
                    string = string + "\n"
                    lines.append(string)
            if string != "":
                lines.append(string + "\n")
        return lines

    def _get_first_eigen_projection(self, iterable):
        try:
            line = self._go_by_keys(iterable, "Eigenvectors required to have negative eigenvalues:", "Eigenvalue     1 is", "Old X")
        except StopIteration:
            self.reset_iters()
            return None
        if "Old X" in line:
            return None
        else:
            result = []
            projections = next(iterable)
            values = next(iterable)
            index = 1
            for projection in projections.split():
                result.append([projection, float(values.split()[index])])
                index = index + 1
            return result

    def _get_berny_section(self):
        part_of_file = []
        try:
            part_of_file = self.get_all_by_key("Berny optimization.")
            part2 = self.get_all_by_key("Berny optimization.")
            part3 = self.get_all_by_key("GradGradGradGradGradGradGrad")
            part_of_file.extend(part2)
            part_of_file.extend(part3)
            yield part_of_file
        except StopIteration:
            self.reset_iters()
            return
        while True:
            part_of_file = []
            try:
                part_of_file = self.get_all_by_key("Berny optimization.")
                part1 = self.get_all_by_key("GradGradGradGradGradGradGrad")
                part_of_file.extend(part1)
                yield part_of_file
            except StopIteration:
                self.reset_iters()
                return

    def _get_first_eigen(self, iterable):
        try:
            line = self._go_by_keys(iterable, "Eigenvalues ---")
        except StopIteration:
            return [0.0, 0.0]
        if not "instead of GDIIS." in line and not "Energy rises --" in line:
            eign = line.split()[2:]
        else:
            eign = [ 0.0, 0.0, 0.0]
        result = []
        result.extend(map(float, eign))
        return result

    def _get_criterion(self, iterable):
        result = []
        _ = self._go_by_keys(iterable, " Item")
        try:
            for i in range(4):
                line = next(iterable)
                result.append([float(line.split()[2]), float(line.split()[3])])
                return result
        except StopIteration:
            return [0.0, 0.0]

    def get_geom(self, iterable):
        _ = self._go_by_keys(iterable, "Input orientation:", "Standard orientation:", "Z-Matrix orientation:")
        iterable = self._skip_lines(iterable, 4)
        lines = self._get_all_by_keys(iterable, "----------------------------------------------")
        charges, coord = self._convert_geom(lines)
        return charges, coord

    def _convert_geom(self, lines):
        iter_lines = iter(lines)
        result_charges = []
        result_charges.extend(map(lambda line: int(line.split()[1]), iter_lines))
        iter_lines = iter(lines)
        result_coord = []
        for line in iter_lines:
            result_coord.append(float(line.split()[3]))
            result_coord.append(float(line.split()[4]))
            result_coord.append(float(line.split()[5]))
        result_coord = np.array(result_coord)
        return result_charges, result_coord

    def _check_termination(self):
        try:
            self.go_to_key("Gaussian 09,")
        except StopIteration:
            return "it_is_not_gauss_file"
        self.reset_iters()
        return "Ok"

    def _check_main_method(self):
        self.go_to_key("#", "#p")
        if "mp2" in self.last_line.lower() or "b2plyp" in self.last_line.lower() or "mpw2lyp" in self.last_line.lower():
            self.main_method = "pt2"
        elif "ccs" in self.last_line.lower():
            self.main_method = "CCS"
        elif "casscf" in self.last_line.lower():
            self.main_method = "casscf"
        elif "td" in self.last_line.lower() or "NRoot"  in self.last_line.lower():
            self.main_method = "excited_states"
        elif "mindo" in self.last_line.lower():
            self.main_method = "empiric"
        else:
            self.main_method = "nopt2"

if __name__ == '__main__':
    with open("opt.out", "r") as gaussin_file:
        g09 = g09_parser(gaussin_file)
    with open("opt.out", "r") as gaussin_file:
        energy = g09.get_energy(gaussin_file)
    print(energy)
    if False:
        with open("opt.out", "r") as gaussin_file:
            charge, coord = g09.get_coord(gaussin_file)
        print(coord)
        with open("opt.out", "r") as gaussin_file:
            force = g09.get_force(gaussin_file)
        print(force)
        with open("opt.out", "r") as gaussin_file:
            orb = g09.get_MO(gaussin_file)
            print(orb)
            hessian = g09.get_hessian(gaussin_file)
            print(hessian)
    with open("opt.out", "r") as gaussin_file:
        crit = g09.get_criteria(gaussin_file)
    print(crit)
    with open("opt.out", "r") as gaussin_file:
        crit = g09.get_EigV_optimization(gaussin_file)
    print(crit)



