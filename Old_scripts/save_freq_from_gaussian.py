with open("opt.out", "r") as input_file:
    freqs = []
    for line in input_file:
        if "incident light, reduced masses (AMU), force constants (mDyne/A)" in line:
            break
    for line in input_file:
        if "Frequencies --" in line:
            l = line.replace("\n","")
            freqs.extend(l.split()[-3:])
with open("freq.txt", "w") as hess_file:
    for freq in freqs:
        hess_file.write(freq + "\n")
