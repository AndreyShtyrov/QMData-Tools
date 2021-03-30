from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser(description=" generate input files")
parser.add_argument("-type", type=str, default="", help="Can choose three stage: opt, scf, charge or check\n"
                                                            "First is to generate pool input files for\n"
                                                            "       You should provide template file that\n"
                                                            "       that content head of gaussian input file\n"
                                                            "Second is to generate from optimized output files\n"
                                                            "       input files for charge calculation\n"
                                                            "       And you should provide template1 file that\n"
                                                            "       content head of gaussian input file in should"
                                                            " content Pop=Mk IOp(6/33=2, 6/41=10, 6/42=17)\n" 
                                                            "Third is to from second stage output file generate RESP\n"
                                                            "       You should add in Path enviroment variable path to"
                                                            " Amber bin\n"
                                                            " Finaly check will print information about progress\n")


CHARGES_TO_SYMBOLS = {
    1: "H",
    6: "C",
    7: "N",
    8: "O"
}


def iter_dir_by_template(template: str, cur_dir: Path):
    for cdir in cur_dir.iterdir():
        if cdir.is_dir():
            if template in cdir.name:
                yield cdir
            else:
                yield from iter_dir_by_template(template, cdir)


def get_number_from_string(line: str):
    result = ""
    for char in line:
        try:
            int(char)
            result = result + char
        except:
            pass
    return result


def iter_file_by_template(template: str, cur_dir: Path):
    for cdir in cur_dir.iterdir():
        if cdir.is_file():
            if template in cdir.name:
                yield cdir
        if cdir.is_dir():
            yield from iter_file_by_template(template, cdir)


def filter_without_key(key, iterate):
    for item in iterate:
        if key not in str(item):
            yield item


def is_terminated(file):
    if file.is_file():
        with open(file, "r") as inp:
            for line in inp:
                if "Error termination request processed" in line:
                    print("Error in " + str(file))
                if "Normal termination of Gaussian" in line:
                    return True
    return False


def get_job_type(file):
    if is_terminated(file):
        acc = 0
        with open(file, "r") as inp:
            for line in inp:
                if acc > 1000:
                    break
                if "#" in line:
                    if "opt" in line.lower():
                        return "opt"
                    elif "pop" in line.lower():
                        return "scf"
                acc = acc + 1
    return None


def check_job_status():
    curr_dir = Path.cwd()
    iter_jobs = iter_file_by_template(".xyz", curr_dir)
    total_number = 0
    for _ in iter_jobs:
        total_number = total_number + 1
    optimized_jobs = 0
    iter_opt_jobs = iter_file_by_template("opt.out", curr_dir)
    for cfile in iter_opt_jobs:
        if get_job_type(cfile) == "opt":
            optimized_jobs = optimized_jobs + 1
    iter_scf_jobs = iter_file_by_template("opt.out", curr_dir)
    scf_jobs_number = 0
    for cfile in iter_scf_jobs:
        if get_job_type(cfile) == "scf":
            scf_jobs_number = scf_jobs_number + 1
    print(" Optimized stucturs " + str(optimized_jobs) + " from " + str(total_number))
    print(" Charges calculated " + str(scf_jobs_number) + " from " + str(total_number))


def creat_optimisation():
    temp_inp = []
    temp_file = Path.cwd() / "template"
    with open(temp_file, "r") as inp:
        temp_inp.extend(inp.readlines())
    curr_dir = Path.cwd()
    iter_files = iter_file_by_template("xyz", curr_dir)
    for cfile in iter_files:
        temp_inp1 = temp_inp[:]
        with open(cfile, "r") as xyz:
            temp_inp1.extend(xyz.readlines())
            temp_inp1.append("\n")
        cal_dir = cfile.parent / (cfile.name.replace(".xyz", "") + "conform")
        cal_dir.mkdir(exist_ok=True)
        os.chdir(str(cal_dir.absolute()))
        with open(cal_dir / "opt.inp", "w") as inp:
            inp.writelines(temp_inp1)


def create_cp2k_inputs():
    temp_inp1 = []
    temp_inp2 = []
    temp_file = Path.cwd() / "template_part1"
    with open(temp_file, "r") as inp:
        temp_inp1.extend(inp.readlines())
    temp_file = Path.cwd() / "template_part2"
    with open(temp_file, "r") as inp:
        temp_inp2.extend(inp.readlines())
    curr_dir = Path.cwd()
    iter_files = iter_file_by_template(".out", curr_dir)
    for cfile in iter_files:
        if get_job_type(cfile) == "scf":
            conformation_dir = cfile.parent.parent
            os.chdir(str(conformation_dir / "01-SCF"))
            os.system("get_optimized_geom opt.out")
            cal_dir = conformation_dir / "02-track-cp2k"
            cal_dir.mkdir(exist_ok=True)
            coord_input = []
            with open(str(conformation_dir / "01-SCF" / "coord.xyz"), "r") as coord_inp:
                for line in coord_inp:
                    slipe_line = line.split()
                    nline = CHARGES_TO_SYMBOLS[int(slipe_line[0])] + " " + slipe_line[1] + " "
                    nline = nline + slipe_line[2] + " " + slipe_line[3].replace("\n", "") + "\n"
                    coord_input.append(nline)
            with open(str(cal_dir / "opt.inp"), "w") as output:
                output.writelines(temp_inp1)
                output.writelines(coord_input)
                output.writelines(temp_inp2)




def create_scf():
    temp_inp = []
    temp_file = Path.cwd() / "template1"
    with open(temp_file, "r") as inp:
        temp_inp.extend(inp.readlines())
    curr_dir = Path.cwd()
    iter_files = iter_file_by_template("opt.out", curr_dir)
    for cfile in iter_files:
        if get_job_type(cfile) == "opt":
            substance_dir = cfile.parent.parent
            conformation_dir = cfile.parent
            temp_inp1 = temp_inp[:]
            os.chdir(str(conformation_dir))
            os.system("get_optimized_geom opt.out")
            with open(cfile, "r") as xyz:
                temp_inp1.extend(xyz.readlines())
                temp_inp1.append("\n")
            cal_dir = cfile.parent / "01-SCF"
            cal_dir.mkdir(exist_ok=True)
            os.system("cp " + str(cfile) + " " +
                      str(substance_dir / (conformation_dir.name + "Optimization.out")))
            with open(cal_dir / "opt.inp", "w") as inp:
                inp.writelines(temp_inp1)


def calculate_Resp_charges():
    curr_dir = Path.cwd()
    iter_files = iter_file_by_template("opt.out", curr_dir)
    for cfile in iter_files:
        if get_job_type(cfile) == "scf":
            if "scf" in cfile.parent.name.lower():
                substance_dir = cfile.parent.parent.parent
                conformation_dir = cfile.parent.parent
            else:
                substance_dir = cfile.parent.parent
                conformation_dir = cfile.parent
            os.chdir(str(substance_dir))
            os.system("antechamber -i opt.out -fi gout -o opt.mol2 -fo mol2 -c resp")
            os.system("cp " + str(cfile.parent / "ANTECHAMBER_RESP2.OUT")
                      + " " + str(substance_dir / (conformation_dir.name + "RespCharges.out")))

            
if __name__ == '__main__':
    args = parser.parse_args()
    print(args.type)
    if args.type == "opt":
        creat_optimisation()
    elif args.type == "scf":
        create_scf()
    elif args.type == "charge":
        calculate_Resp_charges()
    elif args.type == "check":
        check_job_status()
    elif args.type == "cp2k_tracks":
        create_cp2k_inputs()

