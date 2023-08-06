__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '1.0.0'

import os
import pathlib as pl
from distutils.dir_util import copy_tree
import typing as tp

from take_forecast import __path__ as take_forecast_path

DEFAULT_PROJECT_DIR = "take_forecast_project"
PROJECT_TEMPLATE_DIR = "project_template"

PATH = tp.Union[pl.Path, str]


def build_project_path(project_path: PATH) -> pl.Path:
    """Build name for new project directory.
    
    Check if directory "take_forecast_project" exists in directory `project_path`.
    If not, return it. If it already exists, return the first directory named
    "take_forecast_project_<number>" that does not exist.
    
    :param project_path: Path to hold project directory.
    :type project_path: ``pathlib.Path`` or ``str``
    :return: Path for the project directory.
    :rtype: ``pathlib.Path``
    """
    new_project_path = initial_project_path = os.path.join(project_path, DEFAULT_PROJECT_DIR)
    k = 1
    while os.path.exists(new_project_path):
        new_project_path = f"{initial_project_path}_{k}"
        k += 1
    return pl.Path(new_project_path)


def build_project_structure(project_path: PATH) -> None:
    """Build directories and files needed to project.
    
    Create the following directories and files:
        * 'conf/': Hold all project configuration files.
        * 'data/': Data persistence directory organized in layers.
        * 'logs/': Hold logs files.
        * '.kedro.yml': Kedro setting for context.
    
    :param project_path: Path where the project structure will be created.
    :type project_path: ``pathlib.Path`` or ``str``
    """
    template_path = os.path.join(take_forecast_path[0], PROJECT_TEMPLATE_DIR)
    copy_tree(str(template_path), str(project_path))
    os.makedirs(os.path.join(project_path, "data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "logs"), exist_ok=True)
