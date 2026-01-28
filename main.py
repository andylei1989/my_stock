import pandas as pd
import akshare as ak
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
import os, json, time, random
from datetime import datetime, timedelta

DATA_FILE = "portfolio_db.json"

class MainScreen(Screen):
    portfolio = ListProperty([])

    def on_enter(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.portfolio = json.load(f)

    def run_professional_analysis(self):
        """修复版分析逻辑"""
        try:
            # 1. 修复接口名：使用 index_zh_a_hist 替代旧接口
            start_date = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
            # 修复：akshare 2025/2026版本建议使用此接口获取基准
            bench_df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date=start_date, end_date="20261231")
            
            # 2. 获取实时行情 (增加延时，解决截图中的连接被重置问题)
            time.sleep(random.uniform(1.0, 2.0))
            stock_spot = ak.stock_zh_a_spot_em()
            price_map = dict(zip(stock_spot['代码'].astype(str), stock_spot['最新价']))
            
            # 3. 计算 Beta 与 年化收益率 (逻辑同前)
            # ... 此处省略具体计算过程 ...

            print("分析完成并已保存")
        except Exception as e:
            # 捕获错误并显示，避免程序闪退
            print(f"数据同步失败: {str(e)}")

class StockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    StockApp().run()
