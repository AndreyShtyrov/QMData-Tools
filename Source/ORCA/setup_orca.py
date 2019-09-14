import pathlib
import tarfile
import os
print("start setting ORCA")
tmp_orca_dir = pathlib.Path("/tmp/orca_tmp", "r")
tarfile = tarfile.open(pathlib.Path.home() / "ORCA-303.tbz")
if not (tmp_orca_dir / "orca_3_0_3_linux_x86-64/ORCA").is_file():
    print("ORCA has not copied on remote node")
    tarfile.extractall(str(tmp_orca_dir))
    os.system("export orca_dir=" + str(tmp_orca_dir) + "/orca_3_0_3_linux_x86-64/")
    if (tmp_orca_dir / "orca_3_0_3_linux_x86-64/ORCA").is_file():
        print("ORCA was copied")
tarfile.close()
print("")
