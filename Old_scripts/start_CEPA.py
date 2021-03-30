from pathlib import Path
import os

def iter_dir_by_template(template : str,cur_dir: Path):
    for dir in cur_dir.iterdir():
        if dir.is_dir():
            if template in dir.name:
                yield dir
            else:
                yield from iter_dir_by_template(template, dir)

def filter_without_key(key, iterate):
    for item in iterate:
        if not key in str(item):
            yield item


current_dir = Path.cwd()
def creat_cepa_inp():
    iter_prot = iter_dir_by_template("-prot", current_dir)
    for dir in iter_prot:
        n_dir = dir / "10-CEPA"
        t_dir = dir / "30-B3lyp"
        if (t_dir / "opt.out").is_file():
            print(str(dir))
            n_dir.mkdir()
            os.chdir(str(t_dir))
            os.system("get_optimized_geom")
            os.chdir(str(dir))
            os.system("cp 30-B3lyp/coord.xyz 10-CEPA/")
            os.chdir(str(n_dir))
            os.system("generate_input -method cepa -mult 1 -charge 1")

    iter_prot = iter_dir_by_template("diprot", current_dir)
    for dir in iter_prot:
        n_dir = dir / "10-CEPA"
        t_dir = dir / "30-B3lyp"
        if (t_dir / "opt.out").is_file():
            print(str(dir))
            n_dir.mkdir()
            os.chdir(str(t_dir))
            os.system("get_optimized_geom")
            os.chdir(str(dir))
            os.system("cp 30-B3lyp/coord.xyz 10-CEPA/")
            os.chdir(str(n_dir))
            os.system("generate_input -method cepa -mult 1 -charge 2")

    iter_trans = iter_dir_by_template("trans", current_dir)
    iter_only_trans = filter_without_key("prot", iter_trans)
    for dir in iter_only_trans:
        n_dir = dir / "10-CEPA"
        t_dir = dir / "30-B3lyp"
        if (t_dir / "opt.out").is_file():
            print(str(dir))
            n_dir.mkdir(exist_ok=True)
            os.chdir(str(t_dir))
            os.system("get_optimized_geom")
            os.chdir(str(dir))
            os.system("cp 30-B3lyp/coord.xyz 10-CEPA/")
            os.chdir(str(n_dir))
            os.system("generate_input -method cepa -mult 1 -charge 0")


def start_jobs():
    iter1 = iter_dir_by_template("trans", current_dir)
    iter2 = filter_without_key("diprot", iter1)
    for dir in iter2:
        cdir = dir / "10-CEPA"
        if cdir.is_dir():
            os.chdir(str(cdir))
            os.system(" bash ~/bin/mORCA3 opt")



def copy_orbs():
    iter = iter_dir_by_template("10-CEPA", current_dir)
    for dir in iter:
        if (dir / "opt.mrci.nat").is_file():
            n_dir = dir.parent
            os.chdir(str(n_dir))
            t_dir = n_dir / "11-CASSCF"
            t_dir.mkdir(exist_ok=True)
            os.system("cp 10-CEPA/coord.xyz 11-CASSCF")
            os.system("cp 10-CEPA/opt.mrci.nat 11-CASSCF/pr_orb.gbw")
            os.chdir(str(t_dir.absolute()))
            name = n_dir.name
            if "01-tr" in name:
                os.system("generate_input  -pgp ORCA -method casscf -n_state 2 -active 12:12 -mult 1 -charge 0")
                os.system("bash ~/bin/mORCA3 opt")
            elif "dipr" in name:
                os.system("generate_input -pgp ORCA -method casscf -n_state 2 -active 12:12 -mult 1 -charge 1")
                os.system("bash ~/bin/mORCA3 opt")
            elif "prot" in name:
                os.system("generate_input -pgp ORCA -method casscf -n_state 2 -active 12:12 -mult 1 -charge 1")
                os.system("bash ~/bin/mORCA3 opt")


copy_orbs()
