import numpy as np

fr = list()
fr2 = list()


def get_freq(file, natoms):
    freqs = []
    if (3 * natoms - 6) % 3 ==0:
        freqs_rows =  int((3 * natoms - 6)/ 3)
    else:
        freqs_rows = int((3 * natoms - 6) / 3) + 1
    with open(file, "r") as inpfile:
        for line in inpfile:
            if "and normal coordinates:" in line:
                break
        for i in range(freqs_rows-1):
            for line in inpfile:
                if "Frequencies" in line:
                    prev_line = line
                    break
            freqs.extend(read_one_row(inpfile, 3, prev_line, natoms))
        for line in inpfile:
            if "Frequencies" in line:
                prev_line = line
                break
        if (3 * natoms - 6) % 3 == 0:
            freqs.extend(read_one_row(inpfile, 3, prev_line, natoms))
        else:
            freqs.extend(read_one_row(inpfile, (3 * natoms - 6) % 3, prev_line, natoms))


def read_one_row(iterable, coutFreq, prev_line, n_atoms):
    if coutFreq == 3:
        fr1 = {"frn": prev_line.split()[-3], "coord": []}
        fr2 = {"frn": prev_line.split()[-2], "coord": []}
        fr3 = {"frn": prev_line.split()[-1], "coord": []}
        for _ in range(n_atoms):
            line = next(iterable)
            if "Red. masses" in line:
                fr1.update({"irm": line.split()[-3]})
                fr2.update({"irm": line.split()[-2]})
                fr3.update({"irm": line.split()[-1]})
            elif "Frc consts" in line:
                fr1.update({"fc": line.split()[-3]})
                fr2.update({"fc": line.split()[-2]})
                fr3.update({"fc": line.split()[-1]})
            elif "IR Inten" in line:
                fr1.update({"ii": line.split()[-3]})
                fr2.update({"ii": line.split()[-2]})
                fr3.update({"ii": line.split()[-1]})
            elif "Atom  AN" in line:
                pass
            else:
                fr1["coord"].extend(line.split()[-9:-6])
                fr2["coord"].extend(line.split()[-6:-3])
                fr3["coord"].extend(line.split()[-3:])
        return [fr1, fr2, fr3]
    elif coutFreq == 2:
        fr1 = {"frn": prev_line.split()[-2], "coord": []}
        fr2 = {"frn": prev_line.split()[-1], "coord": []}
        for _ in range(n_atoms):
            line = next(iterable)
            if "Red. masses" in line:
                fr1.update({"irm": line.split()[-2]})
                fr2.update({"irm": line.split()[-1]})
            elif "Frc consts" in line:
                fr1.update({"fc": line.split()[-2]})
                fr2.update({"fc": line.split()[-1]})
            elif "IR Inten" in line:
                fr1.update({"ii": line.split()[-2]})
                fr2.update({"ii": line.split()[-1]})
            elif "Atom  AN" in line:
                pass
            else:
                fr1["coord"].extend(line.split()[-6:-3])
                fr2["coord"].extend(line.split()[-3:])
        return [fr1,fr2]

    elif coutFreq == 1:
        fr1 = {"frn": prev_line.split()[-1], "coord": []}
        for _ in range(n_atoms):
            line = next(iterable)
            if "Red. masses" in line:
                fr1.update({"irm": line.split()[-1]})
            elif "Frc consts" in line:
                fr1.update({"fc": line.split()[-1]})
            elif "IR Inten" in line:
                fr1.update({"ii": line.split()[-1]})
            elif "Atom  AN" in line:
                pass
            else:
                fr1["coord"].extend(line.split()[-3:])
        return [fr1]


def write_one_row(freqs, output):
    line = " Frequencies --"
    for fr in freqs:
        pass
    output.write()