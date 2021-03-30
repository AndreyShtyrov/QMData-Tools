result = []
acc = 1
with open("from_sub1d-ADDF.xyz", "r") as inputfile:
    for line in inputfile:
        if "(energy" in line:
            energy = line.replace("\n", "").split()[-1]
            energy = energy.replace(")", "")
            result.append(str(acc) + "  " + energy + "\n")
            acc = acc + 1

with open("energy.txt", "w") as outfile:
    outfile.writelines(result)