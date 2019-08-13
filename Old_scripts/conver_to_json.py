import json
import pathlib
import numpy as np




def check_is_covertable_to_json(instance):
    try:
        json.dumps(instance)
        return True
    except TypeError:
        return False

def save_in_json(convert_object):
    prepare_dict = dict()
    try:
        for key, value in convert_object.__dict__.items():
            if check_is_covertable_to_json(value):
                prepare_dict.update({key: value})
            else:
                try:
                    prepare_dict.update({key: save_in_json(value)})
                except AttributeError:
                    prepare_dict.update({key: str(value)})
    except AttributeError:
        key = str(type(convert_object))
        if check_is_covertable_to_json(convert_object):
            value = json.dumps(convert_object)
        else:
            value = str(convert_object)
        prepare_dict.update({key, value})
    return prepare_dict

class template():

    def __init__(self):
        self.d=1
        self.a =2

    def get(self):
        return self.a

class template2(template):

    def __init__(self):
        super().__init__()
        self.tem = template()
        self.c = 3

    def get(self):
        return self.a



temp = template2()
dict2 = save_in_json(temp)
print(dict2)
js = json.dumps(save_in_json(temp), indent=2)
print(js)
pathlib.Path("./tt1").write_text(js)

def read_save_transform(path_to_transformation: pathlib.Path):
    data = json.load(open(path_to_transformation, "r"))
    basis = np.str(data["basis"])
    basis = basis.replace("\n", "").replace("[", "").replace("]]", "")
    result_basis = []
    for item in basis.split("]"):
        result_basis.append([float(i) for i in item.split()])
    struct1 = np.str(data["delta"])
    struct1 = struct1.replace("\n", "").replace("[", "").replace("]", "")
    result_struct1 = [float(i) for i in struct1.split()]
    print(type(struct1))
    return np.array(result_basis), np.array(result_struct1)

def read_save_q(path_to_transformation: pathlib.Path):
    data = json.load(open(path_to_transformation, "r"))
    struct1 = np.str(data["delta"])
    struct1 = struct1.replace("\n", "").replace("[", "").replace("]", "")
    result_struct1 = [float(i) for i in struct1.split()]
    return np.array(result_struct1)

basis, struct1 = read_save_transform(pathlib.Path("./tt"))
print(type(basis))


