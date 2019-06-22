import pathlib

main_path = pathlib.Path.cwd()
main_path.absolute()
list_names = {}
list_col = []
for traj in main_path.iterdir():
    name = traj.name
    if traj.is_dir():
        if not (traj.absolute() / ("Addition_output/" + str(name) + ".md.energies")).is_file():
            col = 0
            for add_dir in map(lambda x: x.absolute(), traj.iterdir()):
                if (add_dir / ("Addition_output/" + str(name) + ".md.energies")).is_file():
                    with open(add_dir / ("Addition_output/" + str(name) + ".md.energies"), "r") as md_file:
                        s = md_file.readlines()
                        col = col + len(s) - 1
        else:
            with open(traj.absolute() / ("Addition_output/" + str(name) + ".md.energies"), "r") as md_file:
                s = md_file.readlines()
                col = len(s) - 1
        list_names.update({name: col})


with open("result.txt", "w") as result_file:
    for name, col in list_names.items():
        result_file.write(name + "  " + str(col) + "\n")

