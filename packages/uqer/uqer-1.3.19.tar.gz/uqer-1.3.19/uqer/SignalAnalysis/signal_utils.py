# -*- coding: UTF-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pandas as pd


REFRESH_RATE_LIST = ['fri', 'month']
REFRESH_RATE_MAP = {}


def _validate_field(field, valid_fields):
    return field in valid_fields


def list_type_check(data_list, type_tuple):
    res = True
    for data in data_list:
        if not isinstance(data, type_tuple):
            res = False
    return res


def print_validate_risk_aversion(risk_aversion):
    if isinstance(risk_aversion,(int,float)) and risk_aversion >= 0:
        return True
    else:
        print("risk_aversion必须为大于等于0的float/int")
        return False


def print_validate_soft_params(soft_params):
    style_factors = ['factor_exposure_BETA', 'factor_exposure_BTOP', 'factor_exposure_EARNYILD',
                     'factor_exposure_GROWTH',
                     'factor_exposure_LEVERAGE', 'factor_exposure_LIQUIDTY', 'factor_exposure_MOMENTUM',
                     'factor_exposure_RESVOL',
                     'factor_exposure_SIZE', 'factor_exposure_SIZENL', 'factor_exposure_LightIndus',
                     'factor_exposure_HouseApp',
                     'factor_exposure_NonFerMetal', 'factor_exposure_Media', 'factor_exposure_CONMAT',
                     'factor_exposure_Textile',
                     'factor_exposure_ELECEQP', 'factor_exposure_Electronics', 'factor_exposure_CHEM',
                     'factor_exposure_Mining',
                     'factor_exposure_Transportation', 'factor_exposure_NonBankFinan', 'factor_exposure_Auto',
                     'factor_exposure_CommeTrade', 'factor_exposure_Utilities', 'factor_exposure_FoodBever',
                     'factor_exposure_AgriForest', 'factor_exposure_Conglomerates', 'factor_exposure_IronSteel',
                     'factor_exposure_MachiEquip', 'factor_exposure_Telecom', 'factor_exposure_Computer',
                     'factor_exposure_RealEstate', 'factor_exposure_Health', 'factor_exposure_AERODEF',
                     'factor_exposure_LeiService', 'factor_exposure_BuildDeco', 'factor_exposure_Bank']
    validation_result = False
    if isinstance(soft_params, pd.DataFrame):
        if soft_params.empty:
            validation_result = True
        elif ['penalty', 'priority'] == list(soft_params.columns) or ['priority', 'penalty'] == list(
                soft_params.columns):
            indexes = list(soft_params.index)
            if set(indexes).issubset(
                    set(['target_risk_limit', 'asset_bound_limit', 'target_turnover_limit'] + style_factors)):
                if len(soft_params) > len(set(soft_params['priority'])):
                    print('soft_params的priority错误,priority不能有重复值')
                else:
                    if list_type_check(soft_params['priority'], (int, float)) and list_type_check(
                            soft_params['penalty'], (int, float)):
                        validation_result = True
                    else:
                        print("priority和penalty的数据类型错误，正确类型为int或float")
            else:
                print("soft_params的index错误,index在以下四个枚举值中：target_risk_limit,asset_bound_limit,factor_exposure_风格名,target_turnover_limit")
        else:
            print("soft_params的column错误,soft_params.columns为['priority','penalty']")
    else:
        print('soft_params数据类型错误,请传入pd.Dataframe类型')
    return validation_result


def print_validate_frequency(freq):
    validation_result = _validate_field(
        freq, ['day', 'week', 'month', 'quarter', 'semi-year'])
    if not validation_result:
        print("frequency参数：%s暂不支持，支持范围：[day/week/month/quarter/semi-year]" % freq)
    return validation_result


def print_validate_universe(univ):
    validation_result = _validate_field(
        univ, ['SH50','HS300', 'ZZ500', 'TLQA', 'ZZ700', 'ZZ800'])
    custom_universe = isinstance(univ, dict)
    validation_result = validation_result or custom_universe
    if not validation_result:
        print('''universe参数：%s暂不支持，支持范围：[SH50/HS300/ZZ500/ZZ700/ZZ800/
        TLQA]或者自定义universe''' % univ)
    return validation_result


def print_validate_benchmark(benchmark):
    validation_result = benchmark is None or _validate_field(
        benchmark, ['SH50','HS300', 'ZZ500', 'TLQA', 'ZZ700', 'ZZ800', 'risk_free'])
    custom_benchmark = isinstance(benchmark, dict)
    validation_result = validation_result or custom_benchmark
    if not validation_result:
        print('''benchmark参数：%s暂不支持，支持范围：None值或者[SH50/HS300/ZZ500/
        ZZ700/ZZ800/TLQA/risk_free]或者自定义benchmark''' % benchmark)
    return validation_result


def print_validate_weight_type(weight_type):
    validation_result = _validate_field(weight_type, ['equal', 'cap', 'risk'])
    if not validation_result:
        print("weight_type参数：%s暂不支持，支持范围：equal/cap/risk" % weight_type)
    return validation_result


def print_validate_select_type(select_type):
    validation_result = _validate_field(select_type, [0, 1])
    if not validation_result:
        print("select_type参数：%s暂不支持，支持范围：0/1" % select_type)
    return validation_result


def print_validate_construct_method(construct_method):
    validation_result = _validate_field(construct_method,
                                        ['simple_long_only',
                                         'simple_long_short',
                                         'ideal', 'limit_active_risk',
                                         'limit_portfolio_risk',
                                         'max_sharpe_ratio'])
    if not validation_result:
        print('''select_type参数：%s暂不支持，支持范围：simple_long_only/
        simple_long_short/ideal/limit_active_risk/limit_portfolio_risk/
        max_sharpe_ratio''' % construct_method)
    return validation_result