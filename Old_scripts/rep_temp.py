from pathlib import Path

def filter_without_key(key, iterate):
    for item in iterate:
        if key not in str(item):
            yield item

def iter_file_by_template(template: str, cur_dir: Path):
    for cdir in cur_dir.iterdir():
        if cdir.is_file():
            if template in cdir.name:
                yield cdir
        if cdir.is_dir():
            yield from iter_file_by_template(template, cdir)


def replace_template_in_file(cfile: Path, template: str, new_template: str):
    result = []
    with open(cfile, "r") as f:
        for line in f:
            if template in line:
                line_split = line.split(template)
                out_line = line_split[0]
                for i in line_split[1:]:
                    out_line = out_line + new_template + i
            else:
                out_line = line
            result.append(out_line)
        with open(cfile, "w") as f:
            f.writelines(result)


if __name__ == '__main__':
    curr_dir = Path.cwd()
    iter_files = iter_file_by_template("opt.inp", curr_dir)
    template = "CHARGE 1"
    new_template = "CHARGE 0"
    for cfile in filter_without_key(".swp", iter_files):
        print(cfile)
        replace_template_in_file(cfile, template, new_template)
