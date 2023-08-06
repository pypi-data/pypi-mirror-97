# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import typing as tp
import warnings as wn
import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    from statsmodels.tsa.statespace.sarimax import SARIMAX, MLEResults, MLEResultsWrapper


KW = tp.Dict[str, tp.Any]
TS = pd.Series
MODEL = tp.Union[MLEResults, MLEResultsWrapper]


def fit_sarima(ts: TS, kwargs: KW) -> MODEL:
    """Fit a SARIMA for data in time series and given hyper parameters.
    
    Model is optimized by maximizing likelihood with Kalman filter.
    Returned object can make predictions at train time or forecast at time before.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param kwargs: Hyper parameters for ``statsmodels.api.tsa.SARIMAX`` as kwargs.
    
        * **order** (``(int, int, int)``) - Order for AR, I and MA.
        * **seasonal_order** (``(int, int, int, int)``) - Seasonality and order for seasonal AR, I and MA.
    :type kwargs: ``dict`` from ``str`` to ``tuple`` of ``int``
    :return: Fitted SARIMA model.
    :rtype: ``statsmodels.api.tsa.statespace.mlemodel.MLEResults``
    """
    with wn.catch_warnings():
        wn.simplefilter('ignore')
        return SARIMAX(ts, **kwargs).fit(disp=False)
