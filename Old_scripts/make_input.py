from gaussian09 import g09_parser

def make_coords(charges, coords):
    result = []
    ndim = len(charges)
    for i in range(ndim):
        line = charges[i] + " {0:.f5} {1:.f5} {2:.f5}\n".format(coords[i*3], coords[i*3+1], coords[i*3+2])
        result.append(line)
    return result

with open("opt.out", "r") as open_input:
    g09_parser(open_input)
    charges, coords = g09_parser.get_last_geom(open_input)
    make_coords(charges, coords)






