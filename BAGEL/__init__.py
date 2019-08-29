from Constants.physics import *
import numpy as np
import json

def convert_geom(charges: np.ndarray, coords: np.ndarray):
    geom = []
    result = dict({"geometry" : geom})
    for i in range(len(charges)):
        line = {"atom": CHARGES_TO_MASS[charges[i]],
                "xyz": [coords[i*3: i*3 + 3]]}
        result["geometry"].append(line)
    return json.dumps(result, indent=2)

if __name__ == '__main__':
    charges = [1, 1]
    coords = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    with open("save.txt", "w") as f:
        f.writelines(convert_geom(charges, coords))
