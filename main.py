import pandas as pd
import akshare as ak
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty
from kivy.utils import platform
import os, json, time, random
from datetime import datetime

# 数据持久化路径
DATA_PATH = "my_portfolio.json"

class MainScreen(Screen):
    portfolio = ListProperty([])

    def on_enter(self):
        self.load_local_data()

    def load_local_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                self.portfolio = json.load(f)

    def save_and_refresh(self, data):
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        self.on_enter()

    def run_professional_analysis(self):
        """执行 Beta 和 年化计算逻辑"""
        try:
            # 获取实时行情
            spot = ak.stock_zh_a_spot_em()
            price_dict = dict(zip(spot['代码'].astype(str), spot['最新价']))
            
            updated_data = self.portfolio
            for item in updated_data:
                code = item['code'].zfill(6)
                if code in price_dict:
                    item['now_price'] = price_dict[code]
                    # 计算天数和年化 (CAGR)
                    days = (datetime.now() - datetime.strptime(item['date'], '%Y-%m-%d')).days or 1
                    profit = (item['now_price'] - item['buy_price']) / item['buy_price']
                    item['cagr'] = f"{( (1+profit)**(365/days) - 1 ) * 100:.2f}%"
            
            self.save_and_refresh(updated_data)
        except Exception as e:
            print(f"Analysis Error: {e}")

class StockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    StockApp().run()
