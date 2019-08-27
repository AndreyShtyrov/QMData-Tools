import pyparsing
from pathlib import Path
import shutil

input_file = Path("opt.out")
template = " Aug 22"
temp_file = Path("t.out")
new_template = " Jun 14"

with open(input_file, "r") as f:
    with open(temp_file, "w") as t_f:
        for line in f:
            if template in line:
                line_split = line.split(template)
                out_line = line_split[0]
                for i in line_split[1:]:
                    out_line = out_line + new_template + i
            else:
                out_line = line
            t_f.write(out_line)

if temp_file.is_file():
    shutil.move(temp_file, input_file)

template = "22-Aug"
new_template = "14-Jun"

with open(input_file, "r") as f:
    with open(temp_file, "w") as t_f:
        for line in f:
            if template in line:
                line_split = line.split(template)
                out_line = line_split[0]
                for i in line_split[1:]:
                    out_line = out_line + new_template + i
            else:
                out_line = line
            t_f.write(out_line)

if temp_file.is_file():
    shutil.move(temp_file, input_file)
