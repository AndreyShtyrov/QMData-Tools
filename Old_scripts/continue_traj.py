import pathlib
import shutil, os

list_of_important_files = []
general_path = pathlib.Path.cwd()

def copy_from_prev_dir(file_name_in: str, file_name_out: str , prev_work_dir : pathlib.Path, curr_work_dir: pathlib.Path):
    if (prev_work_dir/ file_name_in).is_file():
        shutil.copy(str(prev_work_dir/ file_name_in), str(curr_work_dir / file_name_out))



def copy_important_files_for_calc(name: str, prev_work_dir : pathlib.Path, curr_work_dir: pathlib.Path):
    print(name)
    shutil.copy(str(prev_work_dir / (name + ".RunFileLast")), str(curr_work_dir / (name + ".RunFile")))
#    os.system("cp "+ str(prev_work_dir / "RunFileLast") + " " + str(curr_work_dir / "RunFile"))
#    shutil.copy(str(prev_work_dir /( "Addition_output/" + name + ".RasOrb")), str(curr_work_dir / "pr_orb.RasOrb"))
    shutil.copy(str(prev_work_dir / ( name + ".key")), str(curr_work_dir / (name + ".key")))
    shutil.copy(str(prev_work_dir / "OPLS_aa.prm"), str(curr_work_dir / "OPLS_aa.prm"))
    shutil.copy(str(prev_work_dir.parent().parent()/ "template"), str(curr_work_dir / (name + ".input")))


def move_content_in_day1_dir(name: str, traj_dir: pathlib.Path):
    """
    :param name:
    :param traj_dir:
    :return: 0 or 1 if moving was made
    """
    path_to_md_file = traj_dir.absolute() / ("Addition_output/" + name + ".md.energies")
    if path_to_md_file.is_file():
        dst_dir = traj_dir.absolute() / "day1"
        dst_dir.mkdir()
        shutil.copy(traj_dir.absolute(), dst_dir.absolute())
        return 1
    return 0


for traj_dir in general_path.iterdir():
    last_dir = 0
    if traj_dir.is_dir():
        name = traj_dir.name
        for days_dir in traj_dir.iterdir():
            dst_dir = traj_dir / "day1"
            if not dst_dir.is_dir():
                dst_dir.mkdir()
                if last_dir is 0:
                    last_dir = 1
            if not "day" in str(days_dir.name):
                shutil.move(str(days_dir.absolute()), str(dst_dir.absolute()))
            else:
                if last_dir < int(str(days_dir).split("day")[-1]):
                    last_dir = int(str(days_dir).split("day")[-1])
        if not last_dir is 0:
            dst_dir = traj_dir / ("day" + str(last_dir + 1))
            dst_dir.mkdir()
            f1 = traj_dir / ("day" + str(last_dir + 1))
            f2 = traj_dir / ("day" + str(last_dir))
            copy_important_files_for_calc(name, f2, f1)


general_path = pathlib.Path.cwd()
for cdir in general_path.iterdir():
    name = cdir.name
    if (cdir / "day1").is_dir() and (cdir / "day2").is_dir():
        shutil.copy(str(cdir / "day1"/ (name + ".Final.xyz")), str(cdir / "day1"/ (name + "geom120.xyz")))

