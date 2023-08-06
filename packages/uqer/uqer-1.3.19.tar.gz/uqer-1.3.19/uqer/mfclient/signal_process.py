# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import requests
import traceback
import os
import json
import pandas as pd
import numpy as np
import sys
from . signal_process_check import *
from ..uqer import session

from ..config import *


def neutralize(raw_data, target_date, industry_type="SW1", exclude_style_list=[], **kwargs):
    '''
    中性化处理函数

    :param raw_data: [Dict/Series] 输入待处理因子，key为ticker/secID，value为因子值
    :param target_date: [String] 中性化的基准日期，合理输入为调仓前一个交易日，日期格式为'YYYYMMDD'
    :param industry_type: [String] 行业分类选择, 包括申万一级、申万二级, 分别用SW1/SW2表示，默认为SW1
    :param exclude_style_list: [List] 不中性的风格因子，列入其中的因子在做中性化时不考虑，可选值为'BETA', 'RESVOL', 'MOMENTUM',
    'SIZE', 'SIZENL', 'EARNYILD', 'BTOP', 'GROWTH', 'LEVERAGE', 'LIQUIDTY'，分别代表贝塔、残差波动率、动量、市值、非线性市值、
    盈利性、净市率、成长性、杠杆和流动性
    :return: [Dict/Series] 经过中性化处理之后的因子值
    '''
    # Check Input
    raw_data_check(raw_data)
    industry_check(industry_type)
    date_check(target_date)
    if exclude_style_list:
        risk_factor_check(exclude_style_list)

    if len(raw_data) < 11:
        raise InputLengthError('Neutralize input length too short')

    # 遗留参数处理
    if 'risk_module' in kwargs:
        print ("risk_module参数已经不再使用，中性化函数使用通联风险模型")
    # Series to Dict(if raw_data is Series)
    flag = True
    if isinstance(raw_data, pd.Series):
        flag = False
        raw_data = raw_data.to_dict()

    # Ticker to SecID
    isTicker = False
    for k, v in raw_data.items():
        if len(k) == 11:
            isTicker = True
            break
    record_ticker = {}
    if isTicker:
        for k, v in raw_data.items():
            record_ticker[k[:6]] = k
    # Deal with Nan
    record_nan = {}
    input_dict = {}
    for k, v in raw_data.items():
        if isinstance(v, (int, float)) and math.isnan(v):
            record_nan[k[:6]] = v
        elif v == np.inf or v == -np.inf:
            record_nan[k[:6]] = v
        elif isinstance(v, np.generic):
            input_dict[k[:6]] = np.asscalar(v)
        else:
            input_dict[k[:6]] = v

    send_data = {}
    config_dict = {}
    config_dict['date'] = target_date.replace('-', '')
    config_dict['industry_type'] = industry_type
    config_dict['exclude'] = exclude_style_list
    send_data['raw_data'] = input_dict
    send_data['config'] = config_dict
    try:
        r = session.post(EXT_MFHANDLER_HOST + '/neutralize', json=send_data)
    except:
        raise MFNetworkError('Neutralize Network Error')
    result = handle_recv_json(r)

    # Deal with Nan, Add Nan to result
    if record_nan:
        for k, v in record_nan.items():
            result[k] = v

    # Ticker to SecID, change the key of dict
    final_result = {}
    if isTicker:
        for k, v in result.items():
            final_result[record_ticker[k]] = v
    else:
        final_result = result

    # If Series
    if not flag:
        return pd.Series(final_result)
    else:
        return final_result


# @exception_decorator
def standardize(raw_data):
    '''
    正态化处理函数

    :param raw_data: [Dict/Series] 输入待处理因子，key为ticker/secID，value为因子值
    :return: [Dict/Series] 经过正态化处理之后的因子值
    '''
    raw_data_check(raw_data)
    is_series = False
    if isinstance(raw_data, pd.Series):
        is_series = True

    # Local Process
    se_signal = pd.Series(raw_data)
    if isnull(se_signal):
        return se_signal.to_dict()
    std = se_signal.std()
    if std == 0:
        if is_series:
            return se_signal - se_signal[0]
        else:
            return (se_signal - se_signal[0]).to_dict()  # an all-zero Series
    else:
        if is_series:
            return ((se_signal - se_signal.mean()) / float(std))
        else:
            return ((se_signal - se_signal.mean()) / float(std)).to_dict()


# @exception_decorator
def normalize_l1(raw_data):
    '''
    L1范数正则化函数

    :param raw_data: [Dict/Series] 输入待处理因子，key为ticker/secID，value为因子值
    :return: [Dict/Series] 经过L1范数正则化处理之后的因子值
    '''
    is_series = False
    if isinstance(raw_data, pd.Series):
        is_series = True
    raw_data_check(raw_data)

    # Local Process
    se_signal = pd.Series(raw_data)
    if isnull(se_signal):
        return se_signal.to_dict()
    se_signal = se_signal - se_signal.mean()
    sum_sig = se_signal.abs().sum()
    if sum_sig == 0:
        if is_series:
            return se_signal
        else:
            return se_signal.to_dict()
    else:
        if is_series:
            return se_signal / sum_sig
        else:
            return (se_signal / sum_sig).to_dict()


# @exception_decorator
def winsorize(raw_data, win_type='NormDistDraw', n_draw=5, pvalue=0.05):
    '''
    极值处理函数

    :param raw_data: [Dict/Series] 输入待处理因子，key为ticker/secID，value为因子值
    :param win_type: [String] 去极值处理的类型选择, 包括正态分布去极值和分位数去极值，分别为'NormDistDraw'/'QuantileDraw', 默认为前者
    :param n_draw: [int] 正态分布去极值的迭代次数，只有当win_type='NormDistDraw'，更改该参数才有意义；合法输入为正整数，默认值为5
    :param pvalue: [float] 分位数去极值的分位数指定，只有当win_type='QuantileDraw'，更改该参数才有意义；合法输入为(0,1)区间内的浮点数，默认值为0.05
    :return: [Dict/Series] 经过去极值处理之后的因子值
    '''

    is_series = False
    if isinstance(raw_data, pd.Series):
        is_series = True

    raw_data_check(raw_data)
    if win_type not in ['NormDistDraw', 'QuantileDraw']:
        raise InputConfigError('win_type config error')

    # Local Process
    se_signal = pd.Series(raw_data)
    if isnull(se_signal):
        return se_signal.to_dict()

    if not isinstance(pvalue, float):
        raise InputTypeError('pvalue type error')
    if not 0 < pvalue < 1:
        raise InputConfigError('pvalue config error')

    if not isinstance(n_draw, int) or n_draw <= 0:
        raise InputConfigError('n_draw config error')
    if 'maxint' in sys.__dict__ and n_draw > sys.maxint:
        raise InputConfigError('n_draw is larger than sys.maxint')

    if win_type == 'QuantileDraw':
        QD = QuantileDraw(pvalue)
        if is_series:
            return QD.winsorize(se_signal)
        else:
            return QD.winsorize(se_signal).to_dict()
    else:
        NDD = NormDistDraw(n_draw)
        if is_series:
            return NDD.winsorize(se_signal)
        else:
            return NDD.winsorize(se_signal).to_dict()


class QuantileDraw:
    def __init__(self, pvalue):
        self.pvalue = pvalue

    def winsorize(self, signal):
        series = signal.copy()  # do not modify input data
        lowerbound = self.pvalue / 2.    # quantile lowerbound
        upperbound = 1 - self.pvalue / 2.  # quantile upperbound
        bott = pd.Series.quantile(series, lowerbound)
        upper = pd.Series.quantile(series, upperbound)
        series[series < bott] = bott
        series[series > upper] = upper
        return series


class NormDistDraw:
    def __init__(self, n_draw):
        self.n_draw = n_draw

    def winsorize(self, signal):
        series = signal.copy()  # do not modify input data
        for i in range(self.n_draw):
            std = series.std()
            mean = series.mean()
            series[series < mean - 3 * std] = mean - 3 * std
            series[series > mean + 3 * std] = mean + 3 * std
        return series
