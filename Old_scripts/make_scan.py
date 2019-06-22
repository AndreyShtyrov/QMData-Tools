import pathlib


def make_scan(orb_temp_name: str):
    general_path = pathlib.Path.cwd()
    with open(general_path / "template", "r") as tmp_file:
        template = tmp_file.readlines()

    dir_dictionary = {}
    prev_dir = general_path / "orb"
    for cdir in general_path.iterdir():
        if cdir.is_dir():
            if cdir.name != "orb":
                with open(cdir / "opt.input", "w") as inp_file:
                    line = ">>COPY $InpDir/../" + prev_dir.name + "/" + orb_temp_name + " $WorkDir/INPORB"
                    inp_file.write(line + "\n")
                    inp_file.writelines(template)
                prev_dir = cdir


make_scan("INPORB")
