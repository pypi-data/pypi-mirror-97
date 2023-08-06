# -*- coding: utf-8 -*-
__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import warnings as wn
import numpy as np
import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import statsmodels.api as sm
    from statsmodels.tsa.statespace.sarimax import MLEResults

TS = pd.Series
TS2 = tp.Tuple[TS, TS]
DF = pd.DataFrame
MODEL = MLEResults


def split_train_test(ts: TS, r_split: float) -> TS2:
    """Split data into train and test blocks.

    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param r_split: Data fraction to be train.
    :type r_split: ``float``
    :return: Tuple **(ts_train, ts_test)** where:

        * **ts_train** (``pandas.Series``) - Time series with train block.
        * **ts_test** (``pandas.Series``) - Time series with test block.
    :rtype: ``(pandas.Series, pandas.Series)``
    """
    k = int(r_split * len(ts))
    ts_train = ts.iloc[:k]
    ts_test = ts.iloc[k:]
    return ts_train, ts_test


def get_last_timestamp(ts: TS) -> str:
    """Obtain last timestamp of series as formatted string ('%Y-%m-%d').
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :return: Last timestamp.
    :rtype: ``str``
    """
    return pd.Timestamp(ts.index[-1]).strftime('%Y-%m-%d')


def predict_train_series(model: MODEL) -> TS:
    """Predict time series using a fitted SARIMA model for same period as training data.
    
    :param model: Fitted SARIMA model.
    :type model: ``statsmodels.api.tsa.statespace.mlemodel.MLEResults``
    :return: Predictions on training data.
    :rtype: ``pandas.Series``
    """
    return model.predict()


def limit_train_series(ts_true: TS, ts_pred: TS) -> TS2:
    """Limit train series by removing null initial conditions.
    
    :param ts_true: Measured values for time series.
    :type ts_true: ``pandas.Series``
    :param ts_pred: Predicted values for time series.
    :type ts_pred: ``pandas.Series``
    :return: Tuple **(ts_train, ts_test)** where:

        * **ts_true** (``pandas.Series``) - Limited time series with measured values.
        * **ts_pred** (``pandas.Series``) - Limited time series with predicted values.
    :rtype: ``(pandas.Series, pandas.Series)``
    """
    start = next(filter((lambda k: ts_pred[k] != 0), range(len(ts_pred))))
    return ts_true[start:], ts_pred[start:]


def evaluate_error_metrics(ts_true: TS, ts_pred: TS) -> tp.Dict[str, float]:
    """Calculate error metrics on true and predicted time series.
    
    The implemented error metrics are:
        * root mean square error
        * root mean square relative error
        * mean absolute error
        * mean absolute relative error
        * mean error
        * mean relative error
        * autocorrelation error
        * autocorrelation relative error
        * ljung box statistic error
        * ljung box statistic relative error
        * output and prediction correlation
    
    :param ts_true: Measured values for time series.
    :type ts_true: ``pandas.Series``
    :param ts_pred: Predicted values for time series.
    :type ts_pred: ``pandas.Series``
    :return: Error metrics as indicated above.
    :rtype: ``dict`` of ``str`` to ``float``
    """
    kwargs = {'nlags': 1, 'fft': False, 'qstat': True}
    ts_resid = ts_true - ts_pred
    
    with wn.catch_warnings():
        wn.simplefilter('ignore')
        ts_rel_resid = ts_resid / ts_true
        ts_resid_n = ts_resid - ts_resid.mean()
        ts_rel_resid_n = ts_rel_resid - ts_rel_resid.mean()
        ts_true_n = ts_true - ts_true.mean()
        ts_pred_n = ts_pred - ts_pred.mean()
        acf, qstat, pvalue = sm.tsa.stattools.acf(ts_resid_n, **kwargs)
        acf_rel, qstat_rel, pvalue_rel = sm.tsa.stattools.acf(ts_rel_resid_n, **kwargs)
        corr = np.corrcoef(ts_true_n, ts_pred_n)[0, 1]
    
    return {
        'root mean square error': np.sqrt(ts_resid.pow(2).mean()),
        'root mean square relative error': np.sqrt(ts_rel_resid.pow(2).mean()),
        'mean absolute error': ts_resid.abs().mean(),
        'mean absolute relative error': ts_rel_resid.abs().mean(),
        'mean error': ts_resid.mean(),
        'mean relative error': ts_rel_resid.mean(),
        'autocorrelation error': acf[1],
        'autocorrelation relative error': acf_rel[1],
        'ljung box statistic error': qstat[0],
        'ljung box statistic relative error': qstat_rel[0],
        'output and prediction correlation': corr
    }


def report_error_metrics(train_metrics: tp.Dict[str, float], test_metrics: tp.Dict[str, float]) -> DF:
    """Create report of error metrics for train and test series.
    
    The error metrics are indicated as the dataframe index.
    For more details, check ``evaluate`` function.
    
    :param train_metrics: Error metrics for train data.
    :type train_metrics: ``dict``
    :param test_metrics: Error metrics for test data.
    :type test_metrics: ``dict``
    :return: Dataframe with error metrics for train and test.
    :rtype: ``pandas.DataFrame``
    """
    dct_metrics = dict()
    dct_metrics['train'] = list(train_metrics.values())
    dct_metrics['test'] = list(test_metrics.values())
    return pd.DataFrame(dct_metrics, index=train_metrics.keys())
