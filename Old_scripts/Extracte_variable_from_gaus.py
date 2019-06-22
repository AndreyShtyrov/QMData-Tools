import sys
import os


class substance_for_summary():
    def __init__(self, form, Path):
        self.location=Path
        self.method_of_optimization=Path.split('/')[-2].strip('\r\n')
        self.solvent=Path.split('/')[-1].strip('\r\n')
        self.name_of_form=form
        try:
            self.single_point_methods=self.__parse_table_of_methods_single_point_c(Path)
        except Exception as exception_read_methods:
            print(' file with methods not exist in ' + Path)
            quit()
        self.single_point_energy=[]

    def __parse_table_of_methods_single_point_c(self, Path):
        try:
            with open(Path+"/table_of_methods.txt") as file_with_tabble:
                table_of_methods=[]
                table_of_methods.extend(file_with_tabble.readlines())
                return table_of_methods
        except Exception as exception_read_methods:
            return 'no methods'

    def __parse_g09_energy(self, path_to_the_outfile):
        try:
            with open(path_to_the_outfile) as outfile:
                while True:
                    if "UMP2" in path_to_the_outfile:
                        s=next(outfile)
                        if "E(PMP2)=" in s:
                            return float(s.split()[-1].replace("D","E"))
                    else :
                        s=next(outfile)
                        if "SCF Done:" in s:
                            return float(s.split()[4])
        except Exception as exception_read_Energy  :
#            print(exception_read_Energy.args)
            if "could not convert" in exception_read_Energy.args:
                return "Er_C"
            else:
                return "NONE"

    def __parse_molpro_energy(self, path_to_the_outfile):
        try:
            with open(path_to_the_outfile) as outfile:
                while True:
                        s = next(outfile)
                        if "        UCCSD(T)" in s or "    UCCSD(T)-F12" in s:
                            return float(next(outfile).split()[0])
        except Exception as exception_read_Energy:
            #            print(exception_read_Energy.args)
            if "could not convert" in exception_read_Energy.args:
                return "Er_C"
            else:
                return "NONE"

    def __parse_molcas_energy(self, path_to_the_outfile, method):
        try:
            with open(path_to_the_outfile) as outfile:
                while True:
                    if method == "CASSCF" or method == "RASSCF" :
                        s = next(outfile)	
                        if "      Reference energy:" in s:
                            return float(s.split()[-1])
                    elif method == "CASPT2" or method == "RASPT2":
                        s = next(outfile)
                        if "      Total energy:" in s:
                            return float(s.split()[-1])

        except Exception as exception_read_Energy:
            #            print(exception_read_Energy.args)
            if "could not convert" in exception_read_Energy.args:
                return "Er_C"
            else:
                return "NONE"


    def parse_all_single_p_energys(self):
        for method in self.single_point_methods:
            if method.split()[1].strip('\r\n') == "G09":
                self.single_point_energy.append(self.__parse_g09_energy(self.location+"/"+method.split()[0]+"/"+self.name_of_form+"/opt.out"))
            elif method.split()[1].strip('\r\n') == "Molpro":
                self.single_point_energy.append(self.__parse_molpro_energy(self.location+"/"+method.split()[0]+"/"+self.name_of_form+"/opt.out"))
            elif method.split()[1].strip('\r\n') == "Molcas":
                if "CASSCF" in method.split()[0] or "RASSCF" in method.split()[0]:
                    if "CASSCF" in method.split()[0]:
                        self.single_point_energy.append(self.__parse_molcas_energy(
                            self.location + "/" + method.split()[0].replace("CASSCF","CASPT2") + "/" + self.name_of_form + "/opt.log", "CASSCF"))
                    if "RASSCF" in method.split()[0]:
                        self.single_point_energy.append(self.__parse_molcas_energy(
                            self.location + "/" + method.split()[0].replace("RASSCF",
                                    "RASPT2") + "/" + self.name_of_form + "/opt.log","RASSCF"))
                elif "CASPT2" in method.split()[0]:
                    self.single_point_energy.append(self.__parse_molcas_energy(
                        self.location + "/" + method.split()[0] + "/"+ self.name_of_form + "/opt.log","CASPT2"))
                elif "RASPT2" in method.split()[0]:
                    self.single_point_energy.append(self.__parse_molcas_energy(
                        self.location + "/" + method.split()[0] + "/" + self.name_of_form + "/opt.log", "RASPT2"))
        return

    def save_all_single_p_energys(self, path_to_summary_file):
        print(path_to_summary_file)
        previos_date = []
#	print(self.single_point_methods)
        if os.path.isfile(path_to_summary_file):
            print("******************************************************")
            print("summary file exist and it would be rewritted, add form "+ self.name_of_form)
            print("******************************************************")
            with open(path_to_summary_file)as summary_file:
                previos_date.extend(summary_file)
            os.remove(path_to_summary_file)
        else:
            previos_date.append(self.solvent)
            for method in self.single_point_methods:
                previos_date.append(method.split()[0])
#	print(previos_date)

        with open(path_to_summary_file, 'w+') as summary_file:
            s=previos_date[0].strip('\r\n')+" "+self.name_of_form
            summary_file.write(s+'\r\n')
            for i in range(len(self.single_point_methods)):
                s=previos_date[i+1].strip('\r\n')+" "+str(self.single_point_energy[i])
                summary_file.write(s+'\r\n')

print(os.getcwd())

s=substance_for_summary(sys.argv[1],os.getcwd())
s.parse_all_single_p_energys()
s.save_all_single_p_energys(os.getcwd()+'/summary.txt')







