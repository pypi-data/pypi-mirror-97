# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '1.0.0'
__all__ = [
    'transform_name',
    'get_last',
    'transform_to_cumulative',
    'join',
    'format_forecast_info'
]

import typing as tp
import pandas as pd


TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
DF = pd.DataFrame


def transform_name(name: str) -> str:
    """Transform a column name into column name for us SQL standard.
    
    :param name: Column name.
    :type name: ``str``
    :return: Standard column name.
    :rtype: ``str``
    """
    words = name.split(' ')
    first = [words.pop(-1)]
    others = [word.capitalize() for word in words[::-1]]
    return ''.join(first + others)


def get_last(ts: TS) -> tp.Union[int, float]:
    """Get last value of time series.
    
    :param ts: Time series.
    :type ts: ``pandas.Series``
    :return: Last value.
    :rtype: ``int`` or ``float``
    """
    return ts[-1]


def transform_to_cumulative(ts: TS, ts_lower: TS, ts_upper: TS, offset: int) -> TS3:
    """Transform new daily value at month to monthly value.
    
    Before data is new daily value at month, sampled day by day.
    After data is cumulative value at month, sampled day by day.
    Into a month, cumulative value is cumulative sum at new daily value.
    This is done to give interested output.
    
    :param ts: Time series with new daily value.
    :type ts: ``pandas.Series``
    :param ts_lower: Time series with new daily value lower confidence limit.
    :type ts_lower: ``pandas.Series``
    :param ts_upper: Time series with new daily value upper confidence limit.
    :type ts_upper: ``pandas.Series``
    :param offset: Cumulative initial condition.
    :type offset: ``int``
    :return: Time series with cumulative value at month.
    :rtype: ``pandas.Series``
    """
    cumsum = [offset]
    for k, day in enumerate(ts.index.day):
        cumsum.append((day > 1) * cumsum[k] + ts[k])
    ts_cumsum = pd.Series(cumsum[1:], ts.index)
    # TODO: Calculate variance in cumsum
    ts_cumsum_lower = ts_cumsum.copy()
    ts_cumsum_upper = ts_cumsum.copy()
    name = ts.name.split('New ', 1)[1]
    ts_cumsum.name = name
    ts_cumsum_lower.name = 'lower {name}'.format(name=name)
    ts_cumsum_upper.name = 'upper {name}'.format(name=name)
    return ts_cumsum, ts_cumsum_lower, ts_cumsum_upper


def join(*ts_: TS) -> DF:
    """Join all time series into dataframe.
    
    :param ts_: Time series to join.
    :type ts_: ``pandas.Series``
    :return: Dataframe with all time series.
    :rtype: ``pandas.DataFrame``
    """
    return pd.DataFrame({ts.name: ts for ts in ts_})


def format_forecast_info(df: DF, client: str) -> DF:
    """Format forecast dataframe to expected output format to BLiPNomics.
    
    :param df: Dataframe with all time series.
    :type df: ``pandas.DataFrame``
    :param client: Client.
    :type client: ``str``
    :return: Formatted dataframe.
    :rtype: ``pandas.DataFrame``
    """
    today = pd.Timestamp.now().strftime('%Y-%m-%d')
    dateIni = [t.replace(day=1).strftime('%Y-%m-%d') for t in df.index]
    dateEnd = [t.strftime('%Y-%m-%d') for t in df.index]
    predictionDate = len(df) * [today]
    contractName = len(df) * [client]
    map_names = {
        name: transform_name(name)
        for name in df.keys()
    }
    
    df_meta = pd.DataFrame({
        'dateIni': dateIni,
        'dateEnd': dateEnd,
        'predictionDate': predictionDate,
        'contractName': contractName
    })
    df_data = df.reset_index(drop=True).rename(columns=map_names)
    df_formatted = pd.concat([df_meta, df_data], axis=1)
    return df_formatted
