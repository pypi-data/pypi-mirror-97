# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.6.0'

import typing as tp
import pytest
import numpy as np
import pandas as pd
from take_forecast.tune.nodes import _try_default_
from take_forecast.tune.nodes import sarima_find_d
from take_forecast.tune.nodes import sarima_find_s
from take_forecast.tune.nodes import sarima_find_pq_max
from take_forecast.tune.nodes import sarima_find_spq_max
from take_forecast.tune.nodes import sarima_find_best_hp

KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS2 = tp.Tuple[TS, TS]
DF = pd.DataFrame


def return_result(*args, **kwargs):
    return 1


def raise_exception(*args, **kwargs):
    raise ValueError('Invalid.')


@pytest.fixture
def ts() -> TS:
    np.random.seed(0)
    index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
    data = 100 + 20 * np.random.randn(len(index))
    return pd.Series(data, index, name='ts')


@pytest.fixture
def ts_ramp() -> TS:
    np.random.seed(0)
    index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
    data = 100 + 80 * np.linspace(0, 1, len(index)) + 20 * np.random.randn(len(index))
    return pd.Series(data, index, name='ts')


@pytest.fixture
def df(ts, ts_ramp) -> DF:
    return pd.DataFrame({
        'ts': ts,
        'ts_ramp': ts_ramp
    })


def test__try_default() -> None:
    foo = _try_default_(return_result, (ValueError,), -1)
    assert foo() == 1


def test__try_default__on_error() -> None:
    foo = _try_default_(raise_exception, (ValueError,), -1)
    assert foo() == -1


def test__try_default__on_unexpected_error() -> None:
    foo = _try_default_(raise_exception, (IndexError,), -1)
    try:
        foo()
    except ValueError:
        pass


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('threshold', [-3.51])
@pytest.mark.parametrize('d_stop', [0, 1, 10])
def test__sarima_find_d(df: DF, column: str, threshold: float, d_stop: int) -> None:
    ts = df[column]
    ts_stationary, d = sarima_find_d(ts, threshold, d_stop)
    assert isinstance(ts_stationary, pd.Series)
    assert isinstance(d, int)
    assert d >= 0
    pd.testing.assert_index_equal(ts.index, ts_stationary.index)


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('threshold', [9.21])
@pytest.mark.parametrize('s_start', [3, 4, 5])
@pytest.mark.parametrize('s_stop', [10, 50, 1000])
def test__sarima_find_s(df: DF, column: str, threshold: float, s_start: int, s_stop: int) -> None:
    ts = df[column]
    s = sarima_find_s(ts, threshold, s_start, s_stop)
    assert isinstance(s, int)
    assert s >= 0


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('s', [0, 7, 30, 120])
def test__sarima_find_pq_max(df: DF, column: str, s: int) -> None:
    ts = df[column]
    p_max, q_max = sarima_find_pq_max(ts, s)
    assert isinstance(p_max, int)
    assert isinstance(q_max, int)
    assert p_max >= 0
    assert q_max >= 0


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('s', [0, 7, 30])
@pytest.mark.parametrize('n_cycles', [2, 3, 10, 50])
def test__sarima_find_spq_max(df: DF, column: str, s: int, n_cycles: int) -> None:
    ts = df[column]
    P_max, Q_max = sarima_find_spq_max(ts, s, n_cycles)
    assert isinstance(P_max, int)
    assert isinstance(Q_max, int)
    assert P_max >= 0
    assert Q_max >= 0


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('p_max', [0, 1])
@pytest.mark.parametrize('ur', [0, 1])
@pytest.mark.parametrize('q_max', [0, 1])
@pytest.mark.parametrize('criteria', ['aic', 'bic'])
def test__sarima_find_best_hp__non_seasonal(
        df: DF, column: str, p_max: int, ur: int, q_max: int, criteria: str) -> None:
    ts = df[column]
    s, sP_max, sQ_max = 0, 0, 0
    kwargs = sarima_find_best_hp(ts, p_max, ur, q_max, s, sP_max, sQ_max, criteria)
    assert isinstance(kwargs, dict)
    assert len(kwargs) == 1
    assert 'order' in kwargs
    assert isinstance(kwargs['order'], tuple)
    assert all(isinstance(k, int) for k in kwargs['order'])
    assert kwargs['order'][0] in range(p_max + 1)
    assert kwargs['order'][1] in range(ur + 1)
    assert kwargs['order'][2] in range(q_max + 1)


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('p_max', [0, 1])
@pytest.mark.parametrize('ur', [0, 1])
@pytest.mark.parametrize('q_max', [0, 1])
@pytest.mark.parametrize('s', [7])
@pytest.mark.parametrize('sP_max', [0, 1])
@pytest.mark.parametrize('sQ_max', [0, 1])
@pytest.mark.parametrize('criteria', ['aic', 'bic'])
def test__sarima_find_best_hp__seasonal(
        df: DF, column: str, p_max: int, ur: int, q_max: int, s: int,
        sP_max: int, sQ_max: int, criteria: str) -> None:
    ts = df[column]
    kwargs = sarima_find_best_hp(ts, p_max, ur, q_max, s, sP_max, sQ_max, criteria)
    assert isinstance(kwargs, dict)
    assert len(kwargs) == 2
    assert 'order' in kwargs
    assert isinstance(kwargs['order'], tuple)
    assert all(isinstance(k, int) for k in kwargs['order'])
    assert kwargs['order'][0] in range(p_max + 1)
    assert kwargs['order'][1] in range(ur + 1)
    assert kwargs['order'][2] in range(q_max + 1)
    assert 'seasonal_order' in kwargs
    assert isinstance(kwargs['seasonal_order'], tuple)
    assert all(isinstance(k, int) for k in kwargs['seasonal_order'])
    assert kwargs['seasonal_order'][0] in range(sP_max + 1)
    assert kwargs['seasonal_order'][1] == ur - kwargs['order'][1]
    assert kwargs['seasonal_order'][2] in range(sQ_max + 1)
    assert kwargs['seasonal_order'][3] == s
