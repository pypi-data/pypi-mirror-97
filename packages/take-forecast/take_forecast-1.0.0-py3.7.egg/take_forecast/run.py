# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '1.0.0'

import pathlib as pl

from take_forecast.project_context import ProjectContext


def run_package():
    """Run method to run default pipeline."""
    project_context = ProjectContext(pl.Path.cwd())
    project_context.run()


if __name__ == "__main__":
    run_package()
