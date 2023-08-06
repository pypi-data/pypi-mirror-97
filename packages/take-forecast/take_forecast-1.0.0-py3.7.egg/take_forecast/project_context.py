__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '1.0.0'

import typing as tp
import os
import pathlib as pl
import operator as op
import functools as ft

import pandas as pd
from kedro.context import KedroContext
from kedro.pipeline import Pipeline

from take_forecast.pipeline import load_pipeline
from take_forecast.utils import build_project_structure, build_project_path


class ProjectContext(KedroContext):
    """Context class for this project.
    
    When instantiated, creates all necessary directory structure.
    Then the instance can be used to run the project pipelines.
    
    Methods:
        * **change_dir** - Change current working directory to project path.
        * **create_structure** - Create project directories and files.
        * **run_forecast** - Run the forecast pipelines for input time series.
        
    Example:
    ::
    >>> import numpy as np
    >>> import pandas as pd
    >>> from take_forecast import ProjectContext
    >>> np.random.seed(0)
    >>> samples = 60
    >>> x = 100 + 80 * np.linspace(0, 1, samples) + 20 * np.random.randn(samples)
    >>> y = x[:-3] + x[1:-2] + x[2:-1] + x[3:]
    >>> date_end = pd.Timestamp.now()
    >>> date_start = date_end - pd.Timedelta(len(y) - 1, 'd')
    >>> index = pd.date_range(date_start, date_end, freq='d')
    >>> ts = pd.Series(y, index)
    >>> context = ProjectContext()
    >>> results = context.run_forecast(ts)
    """
    
    project_name = 'Forecast'
    project_version = '0.15.9'
    
    def __init__(self, project_path: tp.Union[pl.Path, str] = None, **kwargs: tp.Dict[str, tp.Any]):
        """Create a context object by providing the root of the project and optional
        additional environment parameters.
        
        If 'project_path' is not provided, create the project structure in the current
        working directory. If provided, it must be an existing directory.
        
        Raises:
            FileNotFoundError: If informed 'project_path' does not exist.
        
        :param project_path: Path where the project will be created.
        :type project_path: ``pathlib.Path`` or ``str``
        :param kwargs: Optional parameters passed to base class instance (``kedro.context.KedroContext``).
        :type kwargs: ``dict`` from ``str`` to ``any``
        """
        project_path = self.create_structure(project_path)
        super().__init__(project_path, **kwargs)
    
    @staticmethod
    def create_structure(project_path: tp.Union[pl.Path, str] = None):
        if not project_path:
            project_path = build_project_path(pl.Path.cwd())
            project_path.mkdir(parents=True)
        elif not pl.Path(project_path).exists():
            raise FileNotFoundError(f"Specified project path does not exist: {project_path}")
    
        build_project_structure(project_path)
        return project_path
    
    def change_dir(self):
        """Change directory to project path directory if it is not current directory."""
        if os.getcwd() != str(self.project_path):
            os.chdir(str(self.project_path))
    
    def _get_pipelines(self) -> tp.Dict[str, Pipeline]:
        """Get project pipelines.
        
        :return: All project pipelines.
        :rtype: ``dict`` from ``str`` to ``kedro.pipeline.Pipeline``
        """
        pipelines = dict()
        loader = self.config_loader
        yml = (lambda step: 'pipelines/{step}.yml'.format(step=step))

        pipelines.update(load_pipeline(loader, yml('tune')))
        pipelines.update(load_pipeline(loader, yml('fit')))
        pipelines.update(load_pipeline(loader, yml('predict')))
        pipelines.update(load_pipeline(loader, yml('evaluate')))

        pipelines['__default__'] = ft.reduce(op.add, pipelines.values())
        return pipelines

    @staticmethod
    def _validate_input_data(input_data: pd.Series) -> None:
        """Validate input data according to necessary conditions.
        
        :param input_data: Input time series.
        :type input_data: ``pandas.Series``
        
        :raise TypeError: If content type is not ``pandas.Series``.
        :raise TypeError: If index type is not ``pandas.DatetimeIndex``.
        :raise ValueError: If data is not sorted by index.
        :raise ValueError: If data is not equally distributed.
        """
        if not isinstance(input_data, pd.Series):
            raise TypeError(f"'input_data' must be ``pandas.Series``, but is type {type(input_data)}.")
        if not isinstance(input_data.index, pd.DatetimeIndex):
            raise TypeError(
                f"Index of 'input_data' must be ``pandas.DatetimeIndex``, but is type {type(input_data.index)}."
            )
        first_diff = input_data.index[1:] - input_data.index[:-1]
        if not all(first_diff > pd.Timedelta(0)):
            raise ValueError(f"'input_data' must be sorted by index.")
        second_diff = first_diff[1:] - first_diff[:-1]
        if not all(second_diff == pd.Timedelta(0)):
            raise ValueError(f"'input_data' index must be equally distributed.")

    def _save_input_data(self, input_data: pd.Series) -> None:
        """Save input data to catalog.
        
        :param input_data: Input time series.
        :type input_data: ``pandas.Series``
        """
        self.catalog.save('original_time_series', input_data)
    
    def _update_params(self, params: tp.Dict[str, tp.Any]):
        """Update context parameters.
        
        :param params: Parameters names and values to be updated.
        :type params: ``dict`` from ``str`` to ``any``
        """
        if self._extra_params is None:
            self._extra_params = dict()
        self._extra_params.update(params)
    
    def _get_results(self) -> tp.Dict[str, tp.Any]:
        """Get forecast results.
        
        :return: Returns a report with the following items:
        
            * **forecast** (``pandas.Series``) - Prediction.
            * **forecast_lower** (``pandas.Series``) - Lower limit.
            * **forecast_upper** (``pandas.Series``) - Upper limit.
            * **alpha** (``float``) - Significance level.
            * **error_metrics_report** (``float``) - Train and test error metrics.
            * **model** (``statsmodels.tsa.statespace.mlemodel.MLEResults``) - Fitted SARIMA model.
        
        :rtype: ``dict`` from ``str`` to ``any``
        """
        load = self.catalog.load
        return {
            'forecast': load('predict_forecast'),
            'forecast_lower': load('predict_forecast_lower'),
            'forecast_upper': load('predict_forecast_upper'),
            'alpha': self.params['fc_alpha'],
            'error_metrics_report': load('error_metrics_report'),
            'model': load('fit_sarima')
        }
    
    def run_forecast(self, time_series: pd.Series,
                     params: tp.Optional[tp.Dict[str, tp.Any]] = None) -> tp.Dict[str, tp.Any]:
        """Run the forecast pipelines for time series with informed parameters.
        
        First, change current working directory to project path.
        Then, validate input data and save it, if valid.
        After this, update default parameters if provided.
        Finally, run the pipelines and return structured results.
        
        The project pipelines can be obtained by the read-only property ``pipelines``.
        This methods execute the default pipeline.
        
        :param time_series: Data to train model.
        :type time_series: ``pandas.Series``
        :param params: Forecast parameters. If None, use default values from configuration file.
        If given, update default values.
        :type params: ``dict`` from ``str`` to ``any``
        :return: Structured results with following items:
        
            * **forecast** (``pandas.Series``) - Prediction.
            * **forecast_lower** (``pandas.Series``) - Lower limit.
            * **forecast_upper** (``pandas.Series``) - Upper limit.
            * **alpha** (``float``) - Significance level.
            * **error_metrics_report** (``float``) - Train and test error metrics.
            * **model** (``statsmodels.tsa.statespace.mlemodel.MLEResults``) - Fitted SARIMA model.
        
        :rtype: ``dict`` from ``str`` to ``any``
        """
        self.change_dir()
        self._validate_input_data(time_series)
        self._save_input_data(time_series)
        if params:
            self._update_params(params)
        self.run()
        return self._get_results()
