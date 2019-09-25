from Source.Utils.listanalyser import ListReader
from Source.Common.Config import config
from Source.Common.General_Tools import *
import pathlib


class orca_config(config):
    """
    :param
    method : available casscf, caspt2, nevpt2, hf
    charge : charge of system
    mult : multiplecity of system
    """
    method: int = "casscf"
    charge: int = 0
    mult: int = 1
    active: str = "0:0"
    nprocs = 12
    _path_to_default_settings: pathlib.Path = pathlib.Path.home() / ".default_orca_settings"

    def __init__(self, config: dict = dict()):
        super().__init__(config)
        if pathlib.Path("pr_orb.gbw").is_file() or pathlib.Path("pr_orb.mrci.nat").is_file():
            self.load = True
        else:
            self.load = False
        self._coords = save_geom_xyz(self._ch, self._co)

    def generate_root_line(self):
        line = "! "
        line = line + self.basis + " "
        if self.basis == "3-21g" or self.basis == "6-31g" or self.basis == "6-31g*":
            line = line + "SV/C "
        elif "cc-" in self.basis:
            line = line + self.basis + "/C "

        line = line + "Direct "
        if self.load:
            line = line + "MOread noiter "

        line = line + "\n"
        return line

    def make_scf(self):
        result = ["%scf  maxiter=999\n"]
        if len(self._ch > 50):
            mem = 7500
            diskmem = 34000
        else:
            mem = 5500
            diskmem = 22000
        line = "maxintmem=" + str(999) + "\n"
        result.append(self.line_with_tab(line))
        line = "maxintmem=" + str(mem) + "\n"
        result.append(self.line_with_tab(line))
        line = "maxdisk=" + str(diskmem) + "\n"
        result.append(self.line_with_tab(line))
        line = "end\n"
        result.append(self.line_with_tab(line))
        return result

    def make_casscf(self):
        result = []
        line = "%casscf nel " + self.active.split(":")[0] + " norb " + self.active.split(":")[1]
        line = line + " mult " + str(self.mult) + " nroots " + str(self.n_state) + "\n"
        result.append(line)
        line = "maxiter 110\n"
        result.append(self.line_with_tab(line, 7))
        line = "ci NGuessMat 512\n"
        result.append(self.line_with_tab(line, 7))
        line = "MaxIter 90\n"
        result.append(self.line_with_tab(line, 7))
        line = " end\n"
        result.append(line)
        line = "trafostep RI\n"
        result.append(self.line_with_tab(line, 7))
        line = "gtol 1e-5\n"
        result.append(self.line_with_tab(line, 7))
        line = "end\n"
        result.append(line)
        return result

    def make_cepa(self):
        result = []
        line = "%mrci citype cepa2\n"
        result.append(line)
        result.append("tsel 1e-5\n")
        result.append("natorbiters 1\n")
        result.append("newblock 1 *\n")
        result.append("nroots 1\n")
        result.append("refs cas(0,0) end\n")
        result.append("end\n")
        result.append("end\n")
        return result

    def make_nevpt2(self):
        result = []
        line = "%casscf nel " + self.active.split(":")[0] + " norb " + self.active.split(":")[1]
        line = line + " mult " + str(self.mult) + " nroots " + str(self.n_state) + "\n"
        result.append(line)
        line = "maxiter 110\n"
        result.append(self.line_with_tab(line, 7))
        line = "ci NGuessMat 512\n"
        result.append(self.line_with_tab(line, 7))

        line = " end\n"
        result.append(line)
        line = "nevpt2 true\n"
        result.append(self.line_with_tab(line, 7))
        line = "NEV_CanonStep 1\n"
        result.append(self.line_with_tab(line, 7))

        line = "trafostep RI\n"
        result.append(self.line_with_tab(line, 7))
        line = "gtol 1e-5\n"
        result.append(self.line_with_tab(line, 7))
        line = "end\n"
        result.append(line)
        return result

    def make_plots(self) -> str:
        def line_plot(number, active: bool):
            if number > -1:
                if active:
                    line = "MO(\"AO-" + str(number) + ".cube\"," + str(number) + ",0);\n"
                else:
                    line = "MO(\"O-" + str(number) + ".cube\"," + str(number) + ",0);\n"
                return line
        result = []
        line = "%plots\n"
        result.append(line)
        line = "Format Gaussian_Cube\n"
        result.append(line)
        start_orb = int(self.n_orb - (self.n_el // 2) - (self.charge // 2)) - 4
        end_orb = start_orb + 8 + int(self.active.split(":")[1])
        for i in range(start_orb, end_orb + 1, 1):
            if i >= 0:
                if start_orb + 4 <= i < start_orb + 4 + int(self.active.split(":")[1]):
                    result.append(line_plot(i, True))
                else:
                    result.append(line_plot(i, False))
        line = "end\n"
        result.append(line)
        return result

    def line_with_tab(self, line, tab=5):
        return "{:{}{}}".format(line, '>', tab + len(line))

    def make_add_sp(self):
        result = []
        if self.load:
            if pathlib.Path("./pr_orb.mrci.nat").is_file():
                line = "%moinp \"./pr_orb.mrci.nat\"\n"
            else:
                line = "%moinp \"./pr_orb.gbw\"\n"
            result.append(line)
        result.append("\n")
        if len(self._ch) > 60:
            result.append("%MaxCore 35000\n")
        else:
            result.append("%MaxCore 22000\n")
        result.append("\n")
        result.append("%pal\n")
        if self.method == "cepa":
            result.append("nprocs=" + str(int(self.nprocs // 4)) + "\n")
        else:
            result.append("nprocs=" + str(self.nprocs) + "\n")
        result.append("end\n")
        result.append("\n")
        return result

    def make_alert(self):
        pass

    def make_input_body(self):
        result = []
        result.append(self.generate_root_line())
        result.append("\n")

        result.extend(self.make_add_sp())

        if self.method == "casscf":
            result.extend(self.make_casscf())
        elif self.method == "nevpt2":
            result.extend(self.make_nevpt2())
        elif self.method == "cepa":
            result.extend(self.make_cepa())
        result.append("\n")

        if not self.method == "cepa":
            result.extend(self.make_plots())


        coords = []
        coords.append("*xyz " + str(self.charge) + " " + str(self.mult) + "\n")
        coords.extend(self._coords)
        coords.append("*\n")
        result.extend(coords)

        with open("opt.inp", "w") as f:
            f.writelines(result)
        self.save_values_in_template(pathlib.Path("pr_template"))
        self.show_job_specification()
