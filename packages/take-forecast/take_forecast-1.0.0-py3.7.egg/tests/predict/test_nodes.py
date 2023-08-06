# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import typing as tp
import warnings as wn
import pytest
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.mlemodel import PredictionResultsWrapper
from pytest_mock.plugin import MockFixture
from take_forecast.predict.nodes import predict_series


KW = tp.Dict[str, tp.Any]
TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
MODEL = tp.Any
PREDICTION = PredictionResultsWrapper


@pytest.fixture
def expected_pred():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	data = 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma
	randn = np.random.randn(N)
	conf = np.cumsum(2 * (np.sign(randn) * randn))
	ts = pd.Series(data, index, name='ts')
	lower = pd.Series(data - conf, index, name='lower ts')
	upper = pd.Series(data + conf, index, name='upper ts')
	return ts, lower, upper


@pytest.fixture
def model(mocker: MockFixture, expected_pred):
	expected_ts, expected_lower, expected_upper = expected_pred
	expected_conf_int = pd.DataFrame({
		expected_lower.name: expected_lower,
		expected_upper.name: expected_upper
	}, expected_ts.index)
	mock_orig_endog = mocker.MagicMock()
	mock_orig_endog.name = expected_ts.name
	mock_data = mocker.Mock()
	mock_data.orig_endog = mock_orig_endog
	mock_forecast = mocker.Mock(spec=PREDICTION)
	mock_forecast.predicted_mean = expected_ts
	mock_forecast.conf_int = mocker.Mock(side_effect=(lambda alpha: expected_conf_int))
	mock_model = mocker.Mock(spec=MODEL)
	mock_model.data = mock_data
	mock_model.get_forecast = mocker.Mock(side_effect=(lambda dt: mock_forecast))
	return mock_model


def test__predict_series__using_horizon(model: MODEL, expected_pred: TS3):
	horizon = '365d'
	end = ''
	alpha = 0.05
	expected_ts, expected_lower, expected_upper = expected_pred
	ts, lower, upper = predict_series(model, horizon, end, alpha)
	assert isinstance(ts, TS)
	assert isinstance(lower, TS)
	assert isinstance(upper, TS)
	pd.testing.assert_series_equal(ts, expected_ts)
	pd.testing.assert_series_equal(lower, expected_lower)
	pd.testing.assert_series_equal(upper, expected_upper)
	model.get_forecast.assert_called_once()


def test__predict_series__using_end(model: MODEL, expected_pred: TS3):
	horizon = ''
	end = '2021-12-31'
	alpha = 0.05
	expected_ts, expected_lower, expected_upper = expected_pred
	ts, lower, upper = predict_series(model, horizon, end, alpha)
	assert isinstance(ts, TS)
	assert isinstance(lower, TS)
	assert isinstance(upper, TS)
	pd.testing.assert_series_equal(ts, expected_ts)
	pd.testing.assert_series_equal(lower, expected_lower)
	pd.testing.assert_series_equal(upper, expected_upper)
	model.get_forecast.assert_called_once()
