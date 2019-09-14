from Source.Utils.parser import parser


class gaussian_chk_parser(parser):

    def __init__(self, file):
        super().__init__(file)
        message = self._check_termination()
        if message is not "Ok":
            print(message)
            exit(1)

    def get_hessian(self, iterable):
        self.go_to_key("Cartesian Force Constants")
        part_of_file = self.get_all_by_key("Dipole Moment")

    def get_energy(self):
        self.go_to_key("Total Energy")
        result = self.last_line.split()[-1]
        self.reset_iters()
        return float(result)

    def get_Mo_coeficent(self, start_key_of_orb = "Total Energy"):
        multiplicity = self._get_multiplicity()
        n_basis_function = self._get_number_of_basis_functions()
        self.reset_iters()
        self.go_to_key(start_key_of_orb)
        self.go_to_key(" MO coefficients", "Total SCF Density")
        mo_coefficent = self.get_all_by_key(" MO coefficients", "Total SCF Density")
        alpha_coefficent = self._extract_mo(mo_coefficent, n_basis_function)
        if multiplicity != 1:
            mo_coefficent = self.get_all_by_key("Total SCF Density")
            beta_coefficent = self._extract_mo(mo_coefficent, n_basis_function)
            self.reset_iters()
            return alpha_coefficent, beta_coefficent
        self.reset_iters()
        return alpha_coefficent, None

    def _extract_mo(self, mo_coeficent, n_basis_function):
        array = []
        for line in mo_coeficent:
            array.extend(map(float, line.split()))
        mo_array_iters = iter(array)
        mo_orbitals = []
        trigger = 0
        for coeff in mo_array_iters:
            if trigger == 0:
                mo = []
            if trigger < n_basis_function - 1:
                mo.append(float(coeff))
                trigger = trigger + 1
            else:
                mo.append(float(coeff))
                trigger = 0
                mo_orbitals.append(mo)

        return mo_orbitals

    def _get_multiplicity(self):
        self.go_to_key("Multiplicity                               I")
        return int(self.last_line.split()[-1])

    def _check_termination(self):
        try:
            self.go_to_key("Multiplicity                               I")
        except StopIteration:
            return "it_is_not_gauss_file"
        self.reset_iters()
        return "Ok"

    def _get_number_of_basis_functions(self):
        self.go_to_key("Number of basis functions")
        return int(self.last_line.split()[-1])

if __name__ == '__main__':
    test = gaussian_chk_parser("orb.fchk")
    mo_a, mo_b = test.get_Mo_coeficent("RMS Density")
    energy = test.get_energy()

