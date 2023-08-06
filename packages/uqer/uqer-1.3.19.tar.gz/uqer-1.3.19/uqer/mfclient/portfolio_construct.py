# coding=utf-8

import json
import requests
import numpy as np
from . signal_process_check import *

from ..config import *
from ..uqer import session


def long_only(raw_data, select_type, top_ratio, weight_type, target_date, risk_model='short', industry_type='SW1',
              universe_type='HS300'):
    '''
    只做多组合构建函数

    :param raw_data: [Dict/Series] 输入的因子值，key为ticker/secID，value为因子值
    :param select_type: [int] 行业类型选择，包括分行业(1)和全行业(0)，若选择分行业，则以后所有选股和配权操作均在行业内部计算
    :param top_ratio: [float] 选择比例，合法输入为(0,0.5)区间的浮点数，表示选取前top_ratio*100%的股票
    :param weight_type: [int] 初始权重类型，包括等权重(0), 流通市值权重(1), 风险权重(2), 因子权重(3)，合法输入为[0,3]区间的整数
    :param target_date: [String] 基准日期，合理输入为调仓前一个交易日，日期格式为'YYYYMMDD'
    :param risk_model: [String] 通联风险模型，包括短期、长期和日度，分别用short/long/day表示；当weight_type=2时，可通过该参数选择风险模型类型
    :param industry_type: [String] 行业分类选择, 包括申万一级、申万二级, 分别用SW1/SW2表示，默认为SW1
    当select_type=1时，可通过改变该参数调整行业分类选择
    :param universe_type: [String] 基准选择，包括沪深300、中证500、中证700、中证800，分别用HS300/ZZ500/ZZ700/ZZ800表示, 默认为HS300
    当select_type=1时，可通过改变该参数调整基准选择
    :return: [Dict/Series] 组合构建的结果，key值为ticker/secID, value为组合中的价值权重
    '''

    # Check Input Data
    is_series = False

    if isinstance(raw_data, dict):
        items = raw_data.items
    elif isinstance(raw_data, pd.Series):
        items = raw_data.iteritems
        is_series = True

    raw_data_check(raw_data)
    date_check(target_date)
    industry_check(industry_type)
    universe_type = universe_check(universe_type)

    if risk_model in ['long', 'short', 'day']:
        risk_model = 'datayes_' + risk_model

    if select_type not in [0, 1]:
        raise InputConfigError("select_type config error")

    if weight_type not in range(4):
        raise InputConfigError("weight_type config error")

    if not isinstance(top_ratio, (float, int, np.int64)):
        raise InputTypeError('top_ratio type error')

    if not 0 < top_ratio < 0.5:
        raise InputConfigError("top_ratio config error, should in (0, 0.5)")

    # Ticker to SecID
    isTicker = False
    for k, v in items():
        if len(k) == 11:
            isTicker = True
            break
    record_ticker = {}
    if isTicker:
        for k, v in items():
            record_ticker[k[:6]] = k

    # Deal with Nan
    record_nan = {}
    input_dict = {}
    for k, v in items():
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
    config_dict['select_type'] = select_type
    config_dict['top_ratio'] = top_ratio
    config_dict['weight_type'] = weight_type
    config_dict['date'] = target_date.replace('-', '')
    config_dict['industry_type'] = industry_type
    config_dict['universe_type'] = universe_type
    config_dict['risk_model'] = risk_model
    send_data['raw_data'] = input_dict
    send_data['config'] = config_dict
    send_data['type'] = 'long_only'
    try:
        r = session.post(EXT_MFHANDLER_HOST + '/get_portfolio', json=send_data)
    except:
        raise MFNetworkError('long_only Network Error')
    ret = handle_recv_json(r)
    # Deal with Nan, Add Nan to result
    # if record_nan:
    #     for k, v in record_nan.items():
    #         ret[k] = v

    # Ticker to SecID, change the key of dict
    final_result = {}
    if isTicker:
        for k, v in ret.items():
            final_result[record_ticker[k]] = v
    else:
        final_result = ret

    if is_series:
        return pd.Series(final_result)
    else:
        return final_result


def simple_long_only(raw_data, target_date, industry_type='SW1', universe_type='HSSLL', **kwargs):
    '''
    简单只做多组合构建函数

    :param raw_data: [Dict/Series] 输入的因子值，key为ticker/secID，value为因子值
    :param target_date: [String] 行业中性的基准日期，合理输入为调仓前一个交易日，日期格式为'YYYYMMDD'
    :param industry_type: [String] 行业分类选择, 包括申万一级、申万二级, 分别用SW1/SW2，默认为SW1
    :param universe_type: [String] 基准选择，包括沪深300、中证500、中证700、中证800，分别用HS300/ZZ500/ZZ700/ZZ800表示, 默认为HS300
    :param holding_weight: [Dict] 输入的持仓权重数据，key值为ticker，value值为现有持仓组合中的价值权重
    :return: [Dict/Series] 组合构建的结果，key值为ticker, value为组合中的价值权重
    '''
    # Check Input Data
    is_series = False
    if isinstance(raw_data, dict):
        items = raw_data.items
    elif isinstance(raw_data, pd.Series):
        items = raw_data.iteritems
        is_series = True

    raw_data_check(raw_data)
    industry_check(industry_type)
    universe_type = universe_check(universe_type)
    date_check(target_date)
    # 历史字段的支持
    if 'holding_weight' in kwargs:
        print ("holding_weight参数已经不再使用了，请参考帮助文档")

    # Ticker to SecID
    isTicker = False
    for k, v in items():
        if len(k) == 11:
            isTicker = True
            break
    record_ticker = {}
    if isTicker:
        for k, v in items():
            record_ticker[k[:6]] = k

    # Deal with Nan
    record_nan = {}
    input_dict = {}
    for k, v in items():
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
    config_dict['universe_type'] = universe_type
    send_data['raw_data'] = input_dict
    send_data['config'] = config_dict

    send_data['type'] = 'simple_long_only'
    try:
        r = session.post(EXT_MFHANDLER_HOST + '/get_portfolio', json=send_data)
    except:
        raise MFNetworkError('simple_long_only Network Error')
    ret = handle_recv_json(r)

    # Deal with Nan, Add Nan to result
    # if record_nan:
    #     for k, v in record_nan.items():
    #         ret[k] = v

    # Ticker to SecID, change the key of dict
    final_result = {}
    if isTicker:
        for k, v in ret.items():
            final_result[record_ticker[k]] = v
    else:
        final_result = ret

    if is_series:
        return pd.Series(final_result)
    else:
        return final_result
