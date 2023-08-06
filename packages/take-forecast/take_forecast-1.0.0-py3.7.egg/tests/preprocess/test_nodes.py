# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.5.0'

import pandas as pd
import pytest
from take_forecast.preprocess.nodes import filter_by_client
from take_forecast.preprocess.nodes import format_dataframe
from take_forecast.preprocess.nodes import limit_by_time
from take_forecast.preprocess.nodes import select
from take_forecast.preprocess.nodes import transform_to_new_daily


@pytest.fixture
def index():
	return pd.DatetimeIndex([
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04'),
		pd.Timestamp('2020-01-05')
	], name='dateEnd')


def test__filter_by_client():
	client = 'client1'
	columns = ['ts1', 'ts2', 'ts3']
	df = pd.DataFrame({
		'dateEnd': ['2020-01-01', '2020-02-02', '2020-01-02', '2020-01-03', '2020-01-04'],
		'contractName': ['client1', 'client1', 'client2', 'client1', 'client2'],
		'ts1': [50, 60, 1200, 72, 980],
		'ts2': [40, 56, 1180, 60, 900],
		'ts3': [48, 59, 1190, 72, 950],
		'other_column': ['A', 'B', 'C', 'D', 'E']
	})
	expected_df = pd.DataFrame({
		'dateEnd': ['2020-01-01', '2020-02-02', '2020-01-03'],
		'ts1': [50, 60, 72],
		'ts2': [40, 56, 60],
		'ts3': [48, 59, 72]
	})
	
	df_filtered = filter_by_client(df, client, columns)
	pd.testing.assert_frame_equal(df_filtered, expected_df)


def test__format_dataframe(index: pd.DatetimeIndex):
	df = pd.DataFrame({
		'dateEnd': ['2020-01-02', '2020-01-04', '2020-01-05', '2020-01-03', '2020-01-01'],
		'ts1': [60, 84, 78, 72, 50],
		'ts2': [56, 78, 76, 60, 40],
		'ts3': [59, 81, 78, 72, 48]
	})
	expected_df = pd.DataFrame({
		'ts1': [50, 60, 72, 84, 78],
		'ts2': [40, 56, 60, 78, 76],
		'ts3': [48, 59, 72, 81, 78]
	}, index)
	
	df_formatted = format_dataframe(df)
	pd.testing.assert_frame_equal(df_formatted, expected_df)


def test__limit_by_time(index: pd.DatetimeIndex):
	t_init = index[2]
	df = pd.DataFrame({
		'ts1': [50, 60, 72, 84, 78],
		'ts2': [40, 56, 60, 78, 76],
		'ts3': [48, 59, 72, 81, 78]
	}, index)
	expected_df = pd.DataFrame({
		'ts1': [72, 84, 78],
		'ts2': [60, 78, 76],
		'ts3': [72, 81, 78]
	}, index[2:])
	
	df_limited = limit_by_time(df, t_init)
	pd.testing.assert_frame_equal(df_limited, expected_df)


def test__select(index: pd.DatetimeIndex):
	column = 'ts1'
	df = pd.DataFrame({
		'ts1': [50, 60, 72, 84, 78],
		'ts2': [40, 56, 60, 78, 76],
		'ts3': [48, 59, 72, 81, 78]
	}, index)
	expected_ts = pd.Series([50, 60, 72, 84, 78], index, name=column)
	
	ts = select(df, column)
	pd.testing.assert_series_equal(ts, expected_ts)


def test__transform_to_new_daily():
	index = pd.date_range('2019-12-31', periods=5, freq='d')
	ts = pd.Series([550, 60, 72, 84, 88], index, name='ts')
	expected_new_ts = pd.Series([60, 12, 12,  4], index[1:], name='New ts', dtype=float)
	
	new_ts = transform_to_new_daily(ts)
	pd.testing.assert_series_equal(new_ts, expected_new_ts)
