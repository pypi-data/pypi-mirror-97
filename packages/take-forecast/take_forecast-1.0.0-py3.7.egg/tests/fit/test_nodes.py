# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import warnings as wn
import pytest
import numpy as np
import pandas as pd
with wn.catch_warnings():
	wn.simplefilter('ignore')
	from statsmodels.tsa.statespace.sarimax import MLEResults, MLEResultsWrapper
from take_forecast.fit.nodes import fit_sarima


TS = pd.Series
DF = pd.DataFrame
MODEL = MLEResults, MLEResultsWrapper


@pytest.fixture
def ts():
	np.random.seed(0)
	index = pd.period_range('2020-01-01', '2020-12-31', freq='d')
	N = len(index)
	exp1 = np.logspace(1, 0.5, N)
	exp2 = np.logspace(1, -2, N)
	cos1 = np.cos(np.linspace(0, 10, N) * np.pi)
	cos2 = np.cos(np.linspace(0.25, 15.75, N) * np.pi)
	sigma = np.random.randn(N)
	data = 100 + 8 * exp1 + 16 * exp2 + 12 * cos1 + 6 * cos2 + 15 * sigma
	return pd.Series(data, index, name='ts')


@pytest.mark.parametrize('p', [0, 1])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
def test__fit_sarima__non_seasonal(ts: TS, p: int, d: int, q: int):
	kwargs = {
		'order': (p, d, q)
	}
	model = fit_sarima(ts, kwargs)
	assert isinstance(model, MODEL)


@pytest.mark.parametrize('p', [0, 1])
@pytest.mark.parametrize('d', [0, 1])
@pytest.mark.parametrize('q', [0, 1])
@pytest.mark.parametrize('s', [7])
@pytest.mark.parametrize('P', [0, 1])
@pytest.mark.parametrize('D', [0, 1])
@pytest.mark.parametrize('Q', [0, 1])
def test__fit_sarima__seasonal(ts: TS, p: int, d: int, q: int, s: int, P: int, D: int, Q: int):
	kwargs = {
		'order': (p, d, q),
		'seasonal_order': (P, D, Q, s)
	}
	model = fit_sarima(ts, kwargs)
	assert isinstance(model, MODEL)
