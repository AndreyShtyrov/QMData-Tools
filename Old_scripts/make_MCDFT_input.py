import os
job_name = "opt.inp"
with open(job_name, "w") as outfile:
    path_to_templates = "."
    if os.path.isfile(path_to_templates + "/temp_part1"):
        with open(path_to_templates + "/temp_part1", "r") as part1:
            outfile.writelines(part1.readlines())
    else:
        print("uncorrect path to template")
        exit(1)
    if os.path.isfile("./p.3.pc"):
        with open("./p.3.pc", "r") as charges:
            iter_chages = iter(charges)
            line = next(iter_chages)
            out_line = line.replace("\n", "").split()[0] + "  ANGSTROM\n"
            outfile.write(out_line)
            for line in iter_chages:
                short_line = line.replace("\n", "")
                out_line = short_line.split()[1] + " " + short_line.split()[2] + " " + short_line.split()[3] + " " + short_line.split()[0]
                out_line = out_line + " 0.0 0.0 0.0\n"
                outfile.write(out_line)
        outfile.write("End  of  Input\n")
    else:
        print("not p.3.pc file")
        exit(1)
    if os.path.isfile(path_to_templates + "/temp_part2"):
        with open(path_to_templates + "/temp_part2", "r") as part1:
            outfile.writelines(part1.readlines())
    else:
        print("uncorrect path to template")
        exit(1)



