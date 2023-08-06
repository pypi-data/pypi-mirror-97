# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.10.0'

import itertools as it
import typing as tp
import warnings as wn
import numpy as np
import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import statsmodels.api as sm


KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS2 = tp.Tuple[TS, TS]


def _try_default_(function: tp.Callable, exceptions: tp.Tuple[tp.Type], default: tp.Any) -> tp.Callable:
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except exceptions:
            return default
    return decorator


def sarima_find_d(ts: TS, threshold: float, d_stop: int) -> tp.Tuple[TS, int]:
    """Find best estimated number of unit roots.
    
    This test uses Augmented Dickey Fuller test to check stationarity.
    Each time the tests finds transitory, witch means unit roots presence, take difference.
    Number of differences up to stationarity is estimated number of unit roots.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param threshold: Threshold for Dickey Fuller.
    :type threshold: ``float``
    :param d_stop: Maximum number of differences to take.
    :type d_stop: ``int``
    :return: Tuple **(ts_stationary, d)**, where:
    
        * **ts_stationary** (``pandas.Series``) - Stationary time series.
        * **d** (``int``) - Estimated number of unit roots.
    :rtype: ``(pandas.Series, int)``
    """
    ts = ts.dropna()
    for d in range(d_stop):
        adf, *_ = sm.tsa.adfuller(ts[d:])
        if adf < threshold:
            return ts, d
        ts = ts.diff()
    return ts, d_stop


def sarima_find_s(ts: TS, threshold: float, s_start: int, s_stop: int) -> int:
    """Find best seasonal period.
    
    This test uses Jung Box at first two cycles and check maximum Q statistics for seasonal period.
    If all Jung Box Q statistics is lower that threshold, time series has no seasonality.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param threshold: Threshold for Jung Box Q statistics.
    :type threshold: ``float``
    :param s_start: Start for seasonal period in test.
    :type s_start: ``int``
    :param s_stop: Stop for seasonal period in test.
    :type s_stop: ``int``
    :return: Seasonality. If not seasonal, return 0.
    :rtype: ``int``
    """
    ts = ts.dropna()
    s_stop = min(s_stop, ts.shape[0] // 4)
    nlags = 2 * s_stop
    n = len(ts)
    s = 0
    Q_max = 0
    for s_ in range(s_start, s_stop):
        ts_mean = ts.rolling(3 * s_, 1, center=True).mean()
        ts_std = ts.rolling(3 * s_, 1, center=True).std()
        ts_norm = (ts - ts_mean) / ts_std
        acf = sm.tsa.acf(ts_norm, alpha=None, nlags=nlags, fft=False)
        mask = np.array([s_, 2 * s_])
        Q = n * (n + 2) * np.sum(np.square(np.clip(acf[mask], 0, np.inf)) / (n - mask))
        if Q > Q_max:
            s = s_
            Q_max = Q
    return s if Q_max > threshold else 0


def sarima_find_pq_max(ts: TS, s: int) -> tp.Tuple[int, int]:
    """Find maximum number of lags for AR and MA model components based on autocorrelation.
    
    AR number of lags is found by partial autocorrelation, where null hypothesis is not more rejected.
    MA number of lags is found by autocorrelation, where null hypothesis is not more rejected.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param s: Seasonal period. If not seasonal, 0.
    :type s: ``int``
    :return: Tuple **(p_max, q_max)** where:
    
        * **p_max** (``int``) - Maximum number of lags for AR.
        * **q_max** (``int``) - Maximum number of lags for MA.
    :rtype: ``(int, int)``
    """
    nlags = (s - 1) if s else min(15, ts.shape[0] // 2)
    ts = ts.dropna()
    acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
    pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
    
    acf_nnull = acf_confint.prod(axis=1) > 0
    pacf_nnull = pacf_confint.prod(axis=1) > 0
    q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
    p_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
    
    return p_max, q_max


def sarima_find_spq_max(ts: TS, s: int, n_cycles: int) -> tp.Tuple[int, int]:
    """Find maximum number of lags for seasonal AR and MA model components based on autocorrelation.
    
    Seasonal AR number of lags is found by partial autocorrelation, where null hypothesis is not more rejected.
    Seasonal MA number of lags is found by autocorrelation, where null hypothesis is not more rejected.
    If time series is not seasonal, returns zero for each one.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param s: Seasonal period. If not seasonal, 0.
    :type s: ``int``
    :param n_cycles: Maximum number of cycles to analyse.
    :type n_cycles: ``int``
    :return: Tuple **(P_max, Q_max)** where:
    
        * **P_max** (``int``) - Maximum number of lags for seasonal AR.
        * **Q_max** (``int``) - Maximum number of lags for seasonal MA.
    :rtype: ``(int, int)``
    """
    if s == 0:
        return 0, 0
    
    n_cycles = min(n_cycles, int(0.5 * ts.shape[0] / s))
    nlags = s * n_cycles
    ts = ts.dropna()
    acf, acf_confint = sm.tsa.stattools.acf(ts, alpha=0.05, nlags=nlags, fft=False)
    pacf, pacf_confint = sm.tsa.stattools.pacf(ts, alpha=0.05, nlags=nlags)
    
    acf = acf[::s]
    acf_confint = acf_confint[::s]
    pacf = pacf[::s]
    pacf_confint = pacf_confint[::s]
    
    acf_nnull = acf_confint.prod(axis=1) > 0
    pacf_nnull = pacf_confint.prod(axis=1) > 0
    acf_nnull[np.abs(acf) > 1] = False
    pacf_nnull[np.abs(pacf) > 1] = False
    Q_max = next(filter(acf_nnull.__getitem__, range(len(acf_nnull) - 1, -1, -1)))
    P_max = next(filter(pacf_nnull.__getitem__, range(len(pacf_nnull) - 1, -1, -1)))
    
    return P_max, Q_max


def sarima_find_best_hp(ts: TS, p_max: int, ur: int, q_max: int, s: int, sP_max: int, sQ_max: int, criteria: str) -> KW:
    """Find best hyper parameters for SARIMA model.
    
    SARIMA is evaluated by AIC or BIC on given time series.
    Best hyper parameters is those minimize information criteria.
    Hyper parameters are:
    
    - order: ``(p, d, q)``
    - seasonal order: ``(P, D, Q, s)``
    
    Where:
    
    - ``p`` is number of lags for AR, or AR order.
    - ``d`` is number of unit roots, or I order.
    - ``q`` is number of lags for MA, or MA order.
    - ``P`` is number of lags for seasonal AR, or sAR order.
    - ``D`` is number of seasonal roots, or sD order.
    - ``Q`` is number of lags for seasonal MA, or sMA order.
    - ``s`` is seasonal period
    
    All combinations are tested in these constraints:
    
    - 0 <= ``p`` <= ``p_max``
    - 0 <= ``q`` <= ``q_max``
    - ``d`` + ``D`` = number of unit roots
    - 0 <= ``d``, ``D`` <= number of unit roots
    - 0 <= ``P`` <= ``P_max``
    - 0 <= ``Q`` <= ``Q_max``
    - ``s`` is given
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :param p_max: Maximum AR order.
    :type p_max: ``int``
    :param ur: Number of unit roots, that is ``d`` + ``D``.
    :type ur: ``int``
    :param q_max: Maximum MA order.
    :type q_max: ``int``
    :param s: Seasonal period.
    :type s: ``int``
    :param sP_max: Maximum sAR order.
    :type sP_max: ``int``
    :param sQ_max: Maximum sMA order.
    :type sQ_max: ``int``
    :param criteria: Criteria to evaluate SARIMA. Can be ``"aic"`` or ``"bic"``.
    :type criteria: ``str``
    :return: Hyper parameters for ``statsmodels.api.tsa.SARIMAX`` as kwargs.
    :rtype: ``dict`` from ``str`` to ``tuple`` of ``int``
    """
    if s:
        ranges = [range(lim + 1) for lim in (p_max, ur, q_max, sP_max, sQ_max)]
        to_kwargs = (lambda p, d, q, P, Q: {
            'order': (p, d, q),
            'seasonal_order': (P, (ur - d), Q, s)
        })
    else:
        ranges = [range(lim + 1) for lim in (p_max, q_max)]
        to_kwargs = (lambda p, q: {
            'order': (p, ur, q)
        })
    evaluate = (lambda kwargs: getattr(sm.tsa.SARIMAX(ts, **kwargs).fit(disp=False), criteria))
    safe_evaluate = _try_default_(evaluate, (np.linalg.LinAlgError,), np.inf)
    with wn.catch_warnings():
        wn.simplefilter('ignore')
        return min(it.starmap(to_kwargs, it.product(*ranges)), key=safe_evaluate)
