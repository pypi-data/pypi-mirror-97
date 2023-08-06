# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '1.0.0'

import typing as tp
import warnings as wn
import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    from statsmodels.tsa.statespace.sarimax import MLEResults


KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
MODEL = MLEResults


def predict_series(model: MODEL, horizon: str, end: str, alpha: float) -> TS3:
    """Predict a time series with a fitted SARIMA model and date up to forecast.
    
    Gives prediction and confidence interval limits.
    
    :param model: Fitted SARIMA model.
    :type model: ``statsmodels.api.tsa.statespace.mlemodel.MLEResults``
    :param horizon: Horizon to define up to forecast since today (format: ``pandas.Timedelta``).
    :type horizon: ``str``
    :param end: End date for forecasting if horizon is None (format: ``pandas.Timestamp``).
    :type end: ``str``
    :param alpha: Significance level for the confidence interval.
    :type alpha: ``float``
    :return: Results in tuple:
    
        * **ts_pred** (``pandas.Series``) - Prediction.
        * **ts_lower** (``pandas.Series``) - Lower limit.
        * **ts_upper** (``pandas.Series``) - Upper limit.
    :rtype: ``(pandas.Series, pandas.Series, pandas.Series)``
    """
    if horizon:
        dt_forecast = pd.Timestamp.now() + pd.Timedelta(horizon)
    else:
        dt_forecast = pd.Timestamp(end)
    
    pred = model.get_forecast(dt_forecast)
    ts_pred = pred.predicted_mean
    conf_int = pred.conf_int(alpha=alpha)
    name = model.data.ynames
    if isinstance(name, list):
        name = name[0]
    ts_lower = conf_int['lower {name}'.format(name=name)]
    ts_upper = conf_int['upper {name}'.format(name=name)]
    ts_pred.name = name
    ts_lower.name = 'lower {name}'.format(name=name)
    ts_upper.name = 'upper {name}'.format(name=name)
    return ts_pred, ts_lower, ts_upper
