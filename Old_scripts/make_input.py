from Source.Gaussian09 import g09_parser
from pathlib import Path
def make_coords(charges, coords):
    result = []
    ndim = len(charges)
    for i in range(ndim):
        line = charges[i] + " {0:.5f} {1:.5f} {2:.5f}\n".format(coords[i*3], coords[i*3+1], coords[i*3+2])
        result.append(line)
    return result

with open("opt.out", "r") as open_input:
    g09 = g09_parser(open_input)
    charges, coords = g09.get_last_geom(open_input)
    coord = make_coords(charges, coords)


temp_path = Path.home()
result = []
with open(temp_path / "temp", "r") as f:
    result = f.readlines()

result.extend(coord)
result.append("\n")
main_path = Path.cwd()
main_path = main_path / "01-RAMAN"
main_path.mkdir()
with open(main_path / "opt.inp", "w") as f:
    f.writelines(result)


