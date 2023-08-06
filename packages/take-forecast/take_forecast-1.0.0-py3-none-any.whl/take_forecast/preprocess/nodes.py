# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '1.0.0'
__all__ = [
    'filter_by_client',
    'format_dataframe',
    'limit_by_time',
    'select',
    'transform_to_new_daily'
]

import typing as tp
import pandas as pd


TS = pd.Series
DF = pd.DataFrame


def filter_by_client(df: DF, client: str, columns: tp.List[str]) -> DF:
    """Filter raw data to get only client data.
    
    :param df: Raw data.
    :type df: ``pandas.DataFrame``
    :param client: Client.
    :type client: ``str``
    :parameter columns: Desired columns separated by comma.
    :type columns: ``list`` of ``str``
    :return: Filtered data.
    :rtype: ``pandas.DataFrame``
    """
    mask = df['contractName'] == client
    columns = ['dateEnd'] + columns
    df_filtered = df.loc[mask, columns]
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def format_dataframe(df: DF) -> DF:
    """Format dataframe to set dateEnd as sorted index as datetime.
    
    :param df: Unformatted data.
    :type df: ``pandas.DataFrame``
    :return: Formatted data.
    :rtype: ``pandas.DataFrame``
    """
    df_formatted = df.copy()
    df_formatted['dateEnd'] = df_formatted['dateEnd'].apply(pd.Timestamp)
    df_formatted = df_formatted.sort_values('dateEnd').set_index('dateEnd')
    return df_formatted


def limit_by_time(df: DF, t_init: str) -> DF:
    """Limit data for since a given initial datetime.
    
    :param df: Unlimited data.
    :type df: ``pandas.DataFrame``
    :param t_init: Initial datetime.
    :type t_init: ``int``
    :return: Limited data.
    :rtype: ``pandas.DataFrame``
    """
    df_limited = df[t_init:]
    return df_limited


def select(df: DF, column: str) -> TS:
    """Select a column from dataframe to give a single time series.
    
    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param column: Column to select.
    :type column: ``str``
    :return: Selected time series.
    :rtype: ``pandas.Series``
    """
    return df[column]


def transform_to_new_daily(ts: TS) -> TS:
    """Transform cumulative value at month to new daily value.
    
    Before data is cumulative value at month, sampled day by day.
    After data is new daily value at month, sampled day by day.
    Into a month, new daily value is difference at cumulative value.
    This is done to make forecast on new daily value instead of cumulative value.
    
    :param ts: Data with cumulative value at month.
    :type ts: ``pandas.Series``
    :return: Data with new daily value at month.
    :rtype: ``pandas.Series``
    """
    ts_diff = ts.diff()[1:]
    ts = ts[1:]
    ts_diff[ts.index.day == 1] = ts[ts.index.day == 1]
    ts_diff.name = 'New {name}'.format(name=ts.name)
    return ts_diff
