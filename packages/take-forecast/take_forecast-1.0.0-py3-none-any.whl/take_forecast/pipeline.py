# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '1.2.0'

import typing as tp
from kedro.config import ConfigLoader
from kedro.pipeline import Pipeline
from take_forecast.utils import build_pipeline


def load_pipeline(loader: ConfigLoader, filename: str,
                  pipeline_name: tp.Optional[str] = None) -> tp.Dict[str, Pipeline]:
    """Load pipeline from config.
    
    :param loader: Config loader.
    :type loader: ``kedro.config.config.ConfigLoader``
    :param filename: Filename to load config.
    :type filename: ``str``
    :param pipeline_name: Pipeline name (optional).
    :type pipeline_name: ``str``
    :return: Pipeline in dict.
    :rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
    """
    pipelines = dict()
    dct_pipeline_setting = loader.get(filename)
    for key, pipeline_setting in dct_pipeline_setting.items():
        pipelines[key] = build_pipeline(pipeline_setting, pipeline_name)
    return pipelines
