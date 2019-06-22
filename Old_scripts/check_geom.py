import os
import sys
import numpy as np
import math as m


def read_geom_from_molcas_input(path_to_dir):
    def _get_geom_from_xyz(file):
        list_of_atoms = []
        with open(file, "r") as coord_file:
            _ = next(coord_file)
            _ = next(coord_file)
            for line in coord_file:
                short_line = line.replace("\n", "")
                if len(short_line.split()) > 2:
                    short_line = line.replace("\n", "").split()[1:4]
                    list_of_atoms.extend(map(float, short_line))
        return np.array(list_of_atoms)


    coord = _get_geom_from_xyz(path_to_dir)

    return coord


def read_geoms_from_molden_file(path_to_file):
    result = []
    with open(path_to_file,"r") as molden_file:
        for line in molden_file:
            if "[GEOMETRIES] (XYZ)" in line:
                break
        trigger = next(molden_file)
        coord = []
        for line in molden_file:
            if trigger in line:
                result.append(np.array(coord))
                coord = []
            elif "[FORCES]" in line:
                break
            else:
                short_line = line.replace("\n", "").split()[1:4]
                coord.extend(map(float, short_line))
        result.append(np.array(coord))
        return result


def read_geom_from_molpro_file(path_to_file):
    result = []
    with open(path_to_file,"r") as input_file:
        for line in input_file:
            if "geometry={angstrom;" in line:
                break
        for line in input_file:
            if "{" in line:
                break
            else:
                short_line = line.replace("\n", "").split()[1:4]
                result.extend(map(float, short_line))
    return np.array(result)


def read_geom_from_gaussina_file(path_to_file):
    result = []
    with open(path_to_file, "r") as gaus_input:
        for line in gaus_input:
            if "#" in line or "#p" in line:
                break
        _ = next(gaus_input)
        line = next(gaus_input)
        if len(line.replace("\n", "")) < 2:
            _ = next(gaus_input)
        else:
            _ = next(gaus_input)
            _ = next(gaus_input)
        line = next(gaus_input)
        while len(line.split()) > 2:
            short_line = line.replace("\n", "").split()[1:4]
            result.extend(map(float, short_line))
            line = next(gaus_input)
    return np.array(result)


def compare_geoms(traectory, path_to_file, program_name):
    if program_name in "G09":
        coord = read_geom_from_gaussina_file(path_to_file + "inp")
    elif program_name in "Molpro":
        coord = read_geom_from_molpro_file(path_to_file + "inp")
    elif program_name in "Molcas":
        coord = read_geom_from_molcas_input(path_to_file + "xyz")
    index = None
    i = 0
    for step_coord in traectory:
        i = i + 1
        difference = coord - step_coord
        min_difference = m.sqrt(difference.dot(difference))
        if min_difference < 0.0001:
            index = i
    return index, len(traectory)


if __name__ == '__main__':
    opt_method = sys.argv[2]
    program_name = sys.argv[3]
    form_name = sys.argv[1]
    list_dirs_comparation = []
    with open("table_of_methods.txt", "r") as table_methods:
        for line in table_methods:
            short_line = line.replace("\n", "").split()
            if "SSCF" in short_line[0]:
                pass
            else:
                list_dirs_comparation.append({"name": short_line[0], "program": short_line[1]})
    if program_name in "molcas":
        traectory_of_optimizations = read_geoms_from_molden_file(opt_method + "/" + form_name + "/Addition_output/opt.geo.molden")
    else:
        print("sorry_script_cannot_read_geom_from_athers_programs_expect_molcas")
        exit(1)
    for method in list_dirs_comparation:
        path_to_file = method["name"] + "/" + form_name + "/opt."
        index, track_len = compare_geoms(traectory_of_optimizations, path_to_file, method["program"])
        print( method["name"] + " " + method["program"] + " : " + str(index) + ", " + str(track_len))
