import os
import sys


def read_geom(line,input):
    result = []
    result.append(line)
    while True:
        line = next(input)
        if "[" in line or line.split()[1] == "":
            return result, line
        else:
            result.append([line.split()[0], line.split()[1], line.split()[2], line.split()[3], line.split()[4], line.split()[5]])


def convert_geom_to_bagel(geom):
    Dictionary_of_atoms = {}
    result = []
    for i in range(len(geom)):
        if i == 0:
            result.append(geom[0].split()[0]+" Angs" +" \n")
        else:
            fist_position = ""
            if geom[i][2] == "1":
                fist_position = " h"
            elif geom[i][2] == "6":
                fist_position = " c"
            elif geom[i][2] == "7":
                fist_position = " n"
            elif geom[i][2] == " 8":
                fist_position = " o"
            if int(geom[i][1]) < 10:
                fist_position = fist_position + "       "+ geom[i][1]
            elif int(geom[i][1]) < 100 and int(geom[i][1]) > 9 :
                fist_position = fist_position + "      " + geom[i][1]
            if int(geom[i][2]) < 10:
                fist_position = fist_position + "       "+ geom[i][2]
            else:
                fist_position = fist_position + "      " + geom[i][2]
            if float(geom[i][3]) < 0:
                fist_position = fist_position + " " + "{:10.8f}".format(float(geom[i][3])/1.889725)
            else:
                fist_position = fist_position + "  " + "{:10.8f}".format(float(geom[i][3]) / 1.889725)
            if float(geom[i][4]) < 0:
                fist_position = fist_position + " " + "{:10.8f}".format(float(geom[i][4])/1.889725)
            else:
                fist_position = fist_position + "  " + "{:10.8f}".format(float(geom[i][4]) / 1.889725)
            if float(geom[i][5]) < 0:
                fist_position = fist_position + " " + "{:10.8f}".format(float(geom[i][5])/1.889725)+"\n"
            else:
                fist_position = fist_position + "  " + "{:10.8f}".format(float(geom[i][5]) / 1.889725) + "\n"
            result.append(fist_position)
            Dictionary_of_atoms.update({geom[i][1]: geom[i][2]})

    return result, Dictionary_of_atoms

def read_level(line, input):
    result = []
    result.append("[5D]"+" \n")
    result.append("[7F]" + " \n")
    result.append("[9G]" + " \n")
    return result

def read_gto(line,input,Dictionary_of_atoms):
    result = []
    result.append(line.split()[0] + " \n")
    while True:
        line = next(input)
        if "[MO]" in line:
            return result, line
        else:
            if len(line.split()) == 1:
                Number_of_atom = line.split()[0]
                result.append(line.split()[0]+ " \n")
                if Dictionary_of_atoms[Number_of_atom] == "1":
                    with open(os.path.dirname(sys.argv[0])+"/lib_bsd/H.gto","r") as bsd:
                        for line2 in bsd:
                            result.append(line2)
                if Dictionary_of_atoms[Number_of_atom] == "6":
                    with open(os.path.dirname(sys.argv[0])+"/lib_bsd/C.gto","r") as bsd:
                        for line2 in bsd:
                            result.append(line2)
                if Dictionary_of_atoms[Number_of_atom] == "7":
                    with open(os.path.dirname(sys.argv[0])+"/lib_bsd/N.gto","r") as bsd:
                        for line2 in bsd:
                            result.append(line2)
                if Dictionary_of_atoms[Number_of_atom] == "8":
                    with open(os.path.dirname(sys.argv[0])+"/lib_bsd/O.gto","r") as bsd:
                        for line2 in bsd:
                            result.append(line2)
                result.append(" \n")




def read_mo(line,input):
    result= []
    result.append(line)
    while True:
        try:
            line = next(input)
        except:
            return  result
        if not(line.split()[0].isdigit()):
            if "Ene=" in line:
                s = " "+ line.split()[0]+ "     "+ "0.00000"+ " \n"
                result.append(s)
            elif "Occup=" in line:
                s = " " + line.split()[0] + "     " + line.split()[1]+ " \n"
                result.append(s)
            elif "Spin=" in line:
                s = " " + line.split()[0] + "     " + line.split()[1]+ " \n"
                result.append(s)
        else:
            s = "       " + line.split()[0] + "       " + line.split()[1] + " \n"
            result.append(s)

def conver_molcas_orb_in_bagel(path,name_input_file):
    with open(path+"/"+name_input_file+".molden","r") as input:
        result = []
        line = next(input)
        if "[MOLDEN FORMAT]" in line:
            result.append(line)
            while True:
                line = next(input)
                if "[ATOMS]" in line:
                    geom, line = read_geom(line,input)
                    geom ,Dictionary_of_atoms = convert_geom_to_bagel(geom)
                    result.extend(geom)
                    level_specification = read_level(line, input)
                if "[GTO]" in line:
                    gto, line = read_gto(line, input,Dictionary_of_atoms)
                    result.extend(gto)
                    result.append(" \n")
                    result.append(" \n")
                    result.extend(level_specification)
                if "MO" in line:
                    MO = read_mo(line,input)
                    result.extend(MO)
                    break
            if os.path.isfile(path+"/"+name_input_file+"converted.molden"):
                os.remove(path+"/"+name_input_file+"converted.molden")

            with open(path+"/"+name_input_file+"converted.molden","w") as output:
                line_steam = iter(result)
                for a in line_steam:
                    output.write(a)
        else:
            print ("file isnot in molden format")
    return

if __name__ == '__main__':
    conver_molcas_orb_in_bagel(".","opt.rasscf")