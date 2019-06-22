import pathlib

main_path = pathlib.Path.cwd()
temp1 = "B3lyp/cc-pVDZ"
temp2 = "B3lyp/6-311++g(d,p)"
def change_file(dir):
    line_list = []
    with open(dir / "opt.inp", "r") as inp_file:
        line_list = inp_file.readlines()
    with open(dir / "opt.inp", "w") as wr_file:
        for line in line_list:
            if temp1 in line:
                line.replace(temp1, temp2)
            wr_file.write(line)

for dir1 in main_path.iterdir():
    if dir1.is_dir():
        for dir2 in dir1.iterdir():
            if "RAMAN" in dir2.name:
                if (dir2 / "opt.inp").is_file():
                    change_file(dir2)

