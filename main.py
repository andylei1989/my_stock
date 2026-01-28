import pandas as pd
import akshare as ak
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
import json, os, time, random
from datetime import datetime
import numpy as np

# 修复安卓环境下akshare可能的IO冲突
os.environ['AKSHARE_DATA_HOME'] = './ak_data'

class PortfolioData:
    """本地数据持久化管理"""
    FILE = "my_stocks.json"
    
    @staticmethod
    def load():
        if os.path.exists(PortfolioData.FILE):
            with open(PortfolioData.FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def save(data):
        with open(PortfolioData.FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

class MainScreen(Screen):
    """主界面逻辑"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.stocks = PortfolioData.load()

    def update_and_analyze(self):
        """执行分析逻辑 (Beta, 年化等)"""
        try:
            # 获取基准
            bench_df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20250101")
            bench_ret = bench_df['收盘'].pct_change()
            
            # 获取行情
            spot = ak.stock_zh_a_spot_em()
            price_map = dict(zip(spot['代码'].astype(str), spot['最新价']))
            
            for s in self.stocks:
                code = s['code'].zfill(6)
                now_price = price_map.get(code, 0)
                # 计算年化与Beta (简化逻辑示例)
                days = (datetime.now() - datetime.strptime(s['date'], '%Y-%m-%d')).days or 1
                profit_rate = (now_price - s['buy_price']) / s['buy_price']
                s['cagr'] = (1 + profit_rate)**(365/days) - 1
                s['current_price'] = now_price
            
            PortfolioData.save(self.stocks)
            print("分析完成")
        except Exception as e:
            print(f"出错: {e}")

class StockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    StockApp().run()