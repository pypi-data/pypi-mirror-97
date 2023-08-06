# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import os

# Local
from .utils import Utils
from .texts import new_class, new_enum, new_license, file, flow, gitignore, readme, setup

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def create_new_class(name: str):
    _, file_path, _, _class = Utils.get_paths_name_class(name)

    Utils.create_file(file_path, new_class(_class))

def create_new_enum(name: str):
    _, file_path, _, _class = Utils.get_paths_name_class(name)

    Utils.create_file(file_path, new_enum(_class))

def create_new_file(name: str):
    _, file_path, _, _ = Utils.get_paths_name_class(name)

    Utils.create_file(file_path, file)

def create_new_flow(name: str):
    _, file_path, _, _ = Utils.get_paths_name_class(name)

    Utils.create_file(file_path, flow)

def create_new_gitignore():
    Utils.create_file(Utils.gitignore_path(), gitignore)

def create_new_readme():
    Utils.create_file(Utils.gitignore_path(), gitignore)

def create_new_subpackage(relative_folder_path: str, create_class: bool = True):
    _, init_file_path, _, _ = Utils.get_paths_name_class(Utils.init_file_path(relative_folder_path))

    if create_class:
        _, _, class_file_name, _class = Utils.get_paths_name_class(relative_folder_path)
        create_new_class(os.path.join(relative_folder_path, class_file_name))

        Utils.create_file(init_file_path, 'from .{} import {}'.format(class_file_name, _class))
    else:
        Utils.create_file(init_file_path, '')


# ---------------------------------------------------------------------------------------------------------------------------------------- #