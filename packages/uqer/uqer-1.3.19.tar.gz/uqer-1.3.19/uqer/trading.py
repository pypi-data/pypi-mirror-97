# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
import datetime as dt

from .config import *
from .utils import convert_date

class LiveTrading(object):
    """优矿模拟交易
    """
    def __init__(self, session):
        super(LiveTrading, self).__init__()
        self.session = session

    def list(self):
        """获取当前模拟交易策略列表
        """
        r = self.session.get(Live_Trading_URL)
        df = pd.DataFrame.from_records(r.json())
        if not df.empty:
            df = df[['id', 'name', 'start_time', 'daily_return', 'total_return']]
            df.start_time = df.start_time.apply(lambda x: dt.datetime.fromtimestamp(x / 1000))

        print ('当前模拟交易个数：{}'.format(len(df)))
        print (df)

        return df

    def orders(self, strategy_id, trade_date=None):
        """单个模拟交易策略详情
            strategy_id: 策略 id
            trade_date: 交易日，如果未指定，则返回当日调仓情况
        """

        url = Live_Order_URL.format(strategy_id)
        if trade_date:
            url = '{}?date={}'.format(url, convert_date(trade_date))
        else:
            url = '{}?calender=1'.format(url)

        try:
            r = self.session.get(url)
            df = pd.DataFrame.from_records(r.json())
            return df
        except:
            print ('获取模拟交易调仓信号错误或者当前没有模拟交易')







            
    