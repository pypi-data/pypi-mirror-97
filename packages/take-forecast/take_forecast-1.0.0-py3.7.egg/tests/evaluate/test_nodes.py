# -*- coding: utf-8 -*-
__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import pytest
import numpy as np
import pandas as pd
from pytest_mock.plugin import MockFixture
from take_forecast.evaluate.nodes import (
    split_train_test, get_last_timestamp, predict_train_series,
    limit_train_series, evaluate_error_metrics, report_error_metrics
)


KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS2 = tp.Tuple[TS, TS]
DF = pd.DataFrame
MODEL = tp.Any
MOCK = MockFixture


@pytest.fixture
def start_date():
    return '2020-01-01'


@pytest.fixture
def end_date():
    return '2020-12-31'


@pytest.fixture
def ts(start_date, end_date) -> TS:
    np.random.seed(0)
    index = pd.date_range(start_date, end_date, freq='d')
    data = 100 + 20 * np.random.randn(len(index))
    return pd.Series(data, index, name='ts')


@pytest.fixture
def ts_ramp(start_date, end_date) -> TS:
    np.random.seed(0)
    index = pd.date_range(start_date, end_date, freq='d')
    data = 100 + 80 * np.linspace(0, 1, len(index)) + 20 * np.random.randn(len(index))
    return pd.Series(data, index, name='ts')


@pytest.fixture
def df(ts, ts_ramp) -> DF:
    return pd.DataFrame({
        'ts': ts,
        'ts_ramp': ts_ramp
    })


@pytest.fixture
def expected_pred(mocker: MockFixture) -> MOCK:
    return mocker.Mock(spec=pd.Series)


@pytest.fixture
def model(mocker: MockFixture, expected_pred: MOCK) -> MOCK:
    model = mocker.Mock()
    model.predict = mocker.Mock(return_value=expected_pred)
    return model


@pytest.fixture
def metric_names() -> tp.List[str]:
    return ['root mean square error',
            'root mean square relative error',
            'mean absolute error',
            'mean absolute relative error',
            'mean error',
            'mean relative error',
            'autocorrelation error',
            'autocorrelation relative error',
            'ljung box statistic error',
            'ljung box statistic relative error',
            'output and prediction correlation']


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('r_split', [0.0, 0.2, 0.5, 0.8, 1.0])
def test__split_train_test(df: DF, column: str, r_split: int) -> None:
    ts = df[column]
    ts_train, ts_test = split_train_test(ts, r_split)
    assert isinstance(ts_train, pd.Series)
    assert isinstance(ts_test, pd.Series)
    assert len(ts_train) == int(r_split * len(ts))
    assert len(ts_test) == len(ts) - len(ts_train)


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
def test__get_last_timestamp(df: DF, column: str, end_date: str) -> None:
    ts = df[column]
    last = get_last_timestamp(ts)
    assert isinstance(last, str)
    assert last == end_date


def test__predict_train_series(model, expected_pred) -> None:
    pred = predict_train_series(model)
    assert isinstance(pred, pd.Series)
    assert pred is expected_pred


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
def test__evaluate_error_metrics(df: DF, column: str, metric_names: tp.List[str]) -> None:
    ts1 = df[column]
    ts2 = ts1 + 20 * np.random.randn(len(ts1))
    metrics = evaluate_error_metrics(ts1, ts2)
    names = list(metrics.keys())
    
    assert isinstance(metrics, dict)
    assert names == metric_names
    for k, metric in metrics.items():
        assert isinstance(metric, float), "Metric {k}, value {m}".format(k=k, m=metric)


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
def test__evaluate_error_metrics__equal_entries(df: DF, column: str, metric_names: tp.List[str]) -> None:
    ts1 = df[column]
    ts2 = ts1
    metrics = evaluate_error_metrics(ts1, ts2)
    names = list(metrics.keys())
    
    assert isinstance(metrics, dict)
    assert names == metric_names
    assert metrics['root mean square error'] == 0
    assert metrics['root mean square relative error'] == 0
    assert metrics['mean absolute error'] == 0
    assert metrics['mean absolute relative error'] == 0
    assert metrics['mean error'] == 0
    assert metrics['mean relative error'] == 0
    assert np.isnan(metrics['autocorrelation error'])
    assert np.isnan(metrics['autocorrelation relative error'])
    assert np.isnan(metrics['ljung box statistic error'])
    assert np.isnan(metrics['ljung box statistic relative error'])
    assert metrics['output and prediction correlation'] == 1


@pytest.mark.parametrize('column', ['ts', 'ts_ramp'])
@pytest.mark.parametrize('num_zeros', [0, 1, 5, 10])
def test__limit_train_series(df: DF, column: str, num_zeros: int) -> None:
    ts = df[column]
    ts1 = ts + 10 * np.random.randn(len(ts))
    ts2 = ts
    ts2[:num_zeros] = 0
    ts1_lim, ts2_lim = limit_train_series(ts1, ts2)
    pd.testing.assert_series_equal(ts1_lim, ts1[num_zeros:])
    pd.testing.assert_series_equal(ts2_lim, ts2[num_zeros:])


def test__report_error_metrics() -> None:
    index = [f'key{i}' for i in range(10)]
    values_train = [np.random.random() for _ in range(10)]
    values_test = [np.random.random() for _ in range(10)]
    metrics_train = dict(zip(index, values_train))
    metrics_test = dict(zip(index, values_test))
    df_ref = pd.DataFrame({'train': values_train, 'test': values_test}, index=index)
    df_metrics = report_error_metrics(metrics_train, metrics_test)
    assert isinstance(df_metrics, pd.DataFrame)
    pd.testing.assert_frame_equal(df_metrics, df_ref)
