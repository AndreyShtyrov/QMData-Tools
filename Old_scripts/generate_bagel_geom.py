import pathlib
import sys, os


def convert_geom(iterable):
    result = []
    for coord in iterable:
        number = int(coord.split()[0])
        x = float(coord.split()[1])
        y = float(coord.split()[2])
        z = float(coord.replace("\n", "").split()[3])
        if number is 1:
            line = "{ \"atom\" :  \"H\" , \"xyz\" : ["+ str(x) +", " + str(y) +", " + str(z) + "]},\n"
        elif number is 6:
            line = "{ \"atom\" :  \"C\" , \"xyz\" : ["+ str(x) +", " + str(y) +", " + str(z) + "]},\n"
        elif number is 7:
            line = "{ \"atom\" :  \"N\" , \"xyz\" : ["+ str(x) +", " + str(y) +", " + str(z) + "]},\n"
        elif number is 8:
            line = "{ \"atom\" :  \"O\" , \"xyz\" : [" + str(x) +", " + str(y) +", " + str(z) + "]},\n"
        result.append(line)
    result[-1] = line.replace("]},\n", "]}]},\n")
    return result


def generate_input():
    temporary_dir = pathlib.Path.home() / "temp"
    os.system("cp " + str(temporary_dir/"part1") + " opt.json")
    file = "opt.xyz"
    with open(file, "r") as f:
        result = convert_geom(f)
    with open("coord.txt", "w") as f:
        f.writelines(result)
    os.system("cat " + "coord.txt" + " >> opt.json")
    os.system("cat " + str(temporary_dir/"part2") + " >> opt.json")


if __name__ == '__main__':
    generate_input()
