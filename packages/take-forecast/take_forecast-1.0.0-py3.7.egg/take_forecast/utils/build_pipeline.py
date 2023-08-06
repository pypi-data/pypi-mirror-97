# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.2.0'

import typing as tp
from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from kedro.utils import load_obj

NODE = tp.Dict[str, tp.Union[str, tp.List[str]]]
PIPELINE = tp.List[NODE]


def build_node(node_setting: NODE, pipeline_name: tp.Optional[str] = None) -> Node:
    """Build a node from settings using standard for a pipeline_name.
    
    In this node, all catalog data, parameters and nodes are prefixes by pipeline_name, except base parameters.
    Node setting is like:
    ::
    >>> node_setting = {'function': 'numpy.sum', 'input': ['x', 'y'], 'output': ['z']}
    >>> node = build_node(node_setting)
    
    :param node_setting: Node settings.
    :type node_setting: ``dict`` from ``str`` to (``str`` or ``list`` of ``str``)
    :param pipeline_name: Pipeline name (optional).
    :type pipeline_name: ``str``
    :return: Node.
    :rtype: ``kedro.pipeline.node.Node``
    """
    func = load_obj(node_setting['func'])
    inputs = node_setting['inputs']
    outputs = node_setting['outputs']
    name = node_setting.get('name', None)
    
    if name is None:
        if pipeline_name is None:
            name = func.__name__
        else:
            name = '{pipeline_name}_{func}'.format(pipeline_name=pipeline_name, func=func.__name__)
    
    if len(inputs) == 0:
        inputs = None
    elif len(inputs) == 1:
        inputs = inputs[0]
    if len(outputs) == 0:
        outputs = None
    elif len(outputs) == 1:
        outputs = outputs[0]
    
    return Node(func, inputs, outputs, name=name)


def build_pipeline(pipeline_setting: PIPELINE, pipeline_name: tp.Optional[str] = None) -> Pipeline:
    """Build a pipeline from settings using standard for a pipeline_name.
    
    In this pipeline, all catalog data, parameters and nodes are prefixes by pipeline_name, except base parameters.
    Pipeline setting is like:
    ::
    >>> pipeline_setting = [
    >>>     {'function': 'numpy.sum', 'input': ['x', 'y'], 'output': ['z']},
    >>>     {'function': 'numpy.power', 'input': ['z'], 'params': ['p'], 'output': ['q']},
    >>> ]
    >>> pipeline = build_pipeline(pipeline_setting, 'pipeline_name')
    
    :param pipeline_setting: Pipeline settings.
    :type pipeline_setting: ``list`` of ``dict`` from ``str`` to (``str`` or ``list`` of ``str``)
    :param pipeline_name: Pipeline name (optional).
    :type pipeline_name: ``str``
    :return: Pipeline.
    :rtype: ``kedro.pipeline.Pipeline``
    """
    return Pipeline([build_node(ns, pipeline_name) for ns in pipeline_setting])
