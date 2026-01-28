import pandas as pd
import akshare as ak
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
import os, json, time, random
from datetime import datetime, timedelta

# 数据存储路径（安卓私有目录）
DATA_FILE = "portfolio.json"

class MainScreen(Screen):
    portfolio = ListProperty([])

    def on_enter(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.portfolio = json.load(f)

    def run_analysis(self):
        try:
            # 1. 获取基准 (修复接口名报错)
            start_date = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
            # 修正后的接口名
            bench_df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date=start_date)
            
            # 2. 获取实时行情 (增加随机延迟防止断连)
            time.sleep(random.uniform(1.0, 2.0))
            stock_spot = ak.stock_zh_a_spot_em()
            price_map = dict(zip(stock_spot['代码'].astype(str), stock_spot['最新价']))
            
            # 3. 更新本地数据逻辑
            for item in self.portfolio:
                code = str(item['code']).zfill(6)
                if code in price_map:
                    item['now_price'] = price_map[code]
                    # 计算逻辑...
            
            # 保存更新
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.portfolio, f, ensure_ascii=False)
            
        except Exception as e:
            print(f"Error: {e}")

class StockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    StockApp().run()
