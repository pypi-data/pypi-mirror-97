from pathlib import PurePath
from typing import List

from pkg_resources import resource_listdir, resource_filename


def get_folder(root_pkg_name: str = __package__, directory: str = "data") -> PurePath:
    """
    Retrieve folder in module: root_pkg_name.directory
    "root_pk_name: Typically my_module.__package__
    """
    path = resource_filename(root_pkg_name, directory)
    return path


def get_files(root_pkg_name: str = __package__, directory: str = "data") -> List[PurePath]:
    """
    Retrieve list of files in module: root_pkg_name.directory
    """
    paths = [
        resource_filename(root_pkg_name, f"{directory}/{filename}")
        for filename in resource_listdir(root_pkg_name, directory)
    ]
    return paths
