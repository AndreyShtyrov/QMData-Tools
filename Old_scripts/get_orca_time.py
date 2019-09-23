import pathlib

curr_dir = pathlib.Path.cwd()

result = []

for dir in curr_dir.iterdir():
    if (dir/"opt.out").is_file():
        with open(dir/"opt.out", "r") as f:
            for line in f:
                if "TOTAL RUN TIME:" in line:
                    result.append(str(dir.name.split("_")[-1]) + " " + line)

with open("result.txt", "w") as f:
    f.writelines(result)