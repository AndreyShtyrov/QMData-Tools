from pathlib import Path

current_file = Path('opt.out')
result = []
with open(current_file, 'r') as f:
    data = {}
    for line in f:
        if '( 1)     EIGENVALUE' in line:
            if 'root1' in data.keys():
                result.append(data)
            data = {}
            data.update({'root1': line.split()[-1]})
        elif '( 2)     EIGENVALUE' in line:
            data.update({'root2': line.split()[-1]})
        elif 'ONIOM: extrapolated energy =' in line:
            data.update({'oniom': line.split()[-1]})

with open('result.txt', "w") as f:
    for data in result:
        if 'oniom' in data.keys():
            #f.write(data['root1'] + " " + data['root2'] + " " + data['oniom'] + "\n")
            f.write(data['root1'] + " " + data['oniom'] + "\n")
