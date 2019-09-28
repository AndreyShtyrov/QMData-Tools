import json
import pathlib
from typing import Union

class data():


    def _load_json(self, file: pathlib.Path)->  Union[list, dict]:
        return json.load(open(file, "r"))

    def _save_json(self, file: pathlib.Path, data: dict):
        js_data = json.dumps(data, indent=2)
        file.write_text(js_data)