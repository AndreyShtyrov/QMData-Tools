import pathlib
import os
import yaml
from Source.Utils.io import config_file

main_path = pathlib.Path.cwd()
cf = config_file()
config_dict = cf.load_file("config.cfg")
config_dict["method"]
test_files_dirs = main_path.iterdir()
for dir in test_files_dirs:
    if dir.is_dir():
        os.chdir(str(dir))
        os.system("generate_config " + str(config_dict["type"]) + " > config")
        config = cf.load_file("config")
        config["wrapper"]["gaussian"]["method"] = config_dict["def_method"]



