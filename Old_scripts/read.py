import math
import numpy as np
from basis_set import basis_vector
from primitive_function import primetive_function


class AO_basis_set():
    def __init__(self, path_to_file):
        self.iterator = self.molden_file(path_to_file)

    def molden_file(self,path_to_file):
        with open(path_to_file,"r") as molen_file:
            return molen_file


class Read_items():
    def __init__(self, file_path):
        self._line_iterator = open(file_path, "r")



    def _open_file(self, file_path):
        with open(file_path, "r") as open_file:
            return open_file

    def get_all_by_key(self, key, stop_block_key):
        result = []
        for line in self._line_iterator:
            if key not in line and stop_block_key not in line:
                result.append(line.replace("\n",""))
            else:
                break
        return result

    def _keys_in_it(self, line, *keys):
        for key in keys:
            if key in line:
                return False, key
        return True, None

    def get_all_by_keys(self, stop_key, *keys):
        result = []
        key = None
        for line in self._line_iterator:
            trigger, key = self._keys_in_it(line, *keys)
            if stop_key in line:
                key = "end"
                break
            if trigger:
                result.append(line.replace("\n", ""))
            else:
                break
        if key is None:
            key = "end"
        return result, key

    def go_to_key(self, *keys):
        triger = False
        for line in self._line_iterator:
            triger, _ = self._keys_in_it( line, *keys)
            if not(triger):
                break


class Read_basis():
    def __init__(self, file_path):
        self._file = Read_items(file_path)
        self.basis = []
        self.coord = self._get_coord()
#        self._file.go_to_key("[GTO]")
        self.atom_number = 0
        self.vector_type = "s"

    def _get_coord(self):
        self._file.go_to_key("[ATOMS]", "[Atoms]")
        part_of_file = self._file.get_all_by_key("[CHARGE] (MULLIKEN)","[GTO]")
        result = []
        for item in part_of_file:
            if len(item.split()) > 3:
                _array = []
                _array.extend(map(float, item.split()[-3:]))
                result.append(np.array(_array))
        return result

    def _indefine_next_vector_type_and_atom_number(self, next_vector_type, next_atom_number):
        self.atom_number = next_atom_number
        if next_vector_type is "p":
            self.vector_type = "px"
        elif next_vector_type is "s":
            self.vector_type = "s"
        elif next_vector_type is "d":
            self.vector_type = "dx2"
        elif next_vector_type is "end":
            self.vector_type = "end"

    def is_number(self, string):
        return  True

    def _format_part_of_text_and_check_current_atom_number(self, part_of_file):
        result = []
        next_atom_number = self.atom_number
        for line in part_of_file:
            if len(line.split()) > 1:
                if self.is_number(line.split()[0]):
                    result.append(line)
            else:
                break
        if len(part_of_file[-1].split()) > 1:
            if "." not in part_of_file[-1].split()[0]:
                try:
                    string = part_of_file[-1].split()[0]
                    next_atom_number = int(string) - 1
                except:
                    next_atom_number = self.atom_number
        else:
            try:
                string = part_of_file[-1].split()[0]
                next_atom_number = int(string) - 1
            except:
                next_atom_number = self.atom_number
        return result, next_atom_number

    def next_vector(self) -> basis_vector:
        self._file.go_to_key("s")
        while self.vector_type is not "end":
            if self.vector_type is "s" or self.vector_type is "px" or self.vector_type is "dx2":
                part_of_file, next_vector_type = self._file.get_all_by_keys("[MO]","s","p","d","f")
                part_of_file, next_atom_number = self._format_part_of_text_and_check_current_atom_number(part_of_file)
            vector = primetive_function( self.coord[self.atom_number])
            _expected_next_vector_type = vector.set_spherical_component(self.vector_type)
            list_of_vectors = []
            for coeff_alpha in part_of_file:
                vector1 = primetive_function(vector.A)
                _ = vector1.set_spherical_component(self.vector_type)
                coeff = float(coeff_alpha.split()[1])
                alpha = float(coeff_alpha.split()[0])
                vector1.set_coeff_alpha(coeff, alpha)
                list_of_vectors.append(vector1)
            yield basis_vector(list_of_vectors)
            if _expected_next_vector_type is "s" or _expected_next_vector_type is _expected_next_vector_type  is "p" or _expected_next_vector_type is "d" or _expected_next_vector_type is"end":
                self._indefine_next_vector_type_and_atom_number(next_vector_type, next_atom_number)
            else:
                self.vector_type = _expected_next_vector_type

    def _define_format(self):
        pass

class Read_MO():
    def __init__(self, file_path):
        self._file = Read_items(file_path)
        self._file.go_to_key("[MO]")
        self._file.go_to_key("Sym=")
        self._end_of_file = False

    def is_number(self, string):
        try:
            int(string)
            return True
        except:
            return False

    def next_mo(self):
        while not self._end_of_file:
            part_of_file, key = self._file.get_all_by_keys("Nope", "Sym=")
            mo_vector = []
            for line in part_of_file:
                if "=" not in line:
                    mo_vector.append(float(line.split()[1]))
            if key is "end":
                self._end_of_file = True
            yield np.array(mo_vector)