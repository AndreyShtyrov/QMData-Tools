import pathlib
import shutil


def get_dir_tree(path: pathlib.Path):
    for cur_dir in path.iterdir():
        if not cur_dir.is_dir():
            yield cur_dir
        else:
            yield from get_dir_tree(cur_dir)
    return

def geom_file_iters(path: pathlib.Path) -> iter:
    molden_geom_file = ""
    for cur_file in get_dir_tree(path):
        if "geo.molden" in cur_file.name:
            molden_geom_file = cur_file
    with open(molden_geom_file, "r") as molden_geom_file:
        for line in molden_geom_file:
            yield line
    return


def get_last_geom(path):
    geom_file = geom_file_iters(path)
    next(geom_file)
    next(geom_file)
    number_geoms = int(next(geom_file).replace("\n",""))
    for line in geom_file:
        if "[GEOMETRIES] (XYZ)" in line:
            break
    coords_number = int(next(geom_file).replace("\n",""))

    for i in range((number_geoms - 1)* (coords_number + 2)):
        _ = next(geom_file)
    _ = next(geom_file)
    result = []
    result.append(str(coords_number) +  "\n")
    result.append("\n")
    for i in range(coords_number):
        result.append(next(geom_file))
    return  result


def restart_calculations():
    general_path = pathlib.Path.cwd()
    new_dir_number = 1
    for cur_dir in general_path.iterdir():
        if cur_dir.is_dir():
            if "-" in cur_dir.name:
                number = int(cur_dir.name.split("-")[0])
                if new_dir_number <= number:
                    new_dir_number = number + 1
    work_dir = general_path / (str(new_dir_number) + "-opt")
    work_dir.mkdir()
    coords = get_last_geom(general_path)
    input_file = ""
    for cur_file in general_path.iterdir():
        if cur_file.is_file():
            if ".inp" in cur_file.name:
                input_file = cur_file
                break
    shutil.copy(str(input_file), str(work_dir/"opt.inp"))
    shutil.copy(str(general_path/"Addition_output/opt.RasOrb"), str(work_dir / "pr_orb.RasOrb"))
    with open( work_dir /"opt.xyz", "w") as out_geom_file:
        out_geom_file.writelines(coords)

if __name__ == '__main__':
    restart_calculations()