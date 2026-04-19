import json, os
import pandas as pd

class AICore:
    def __init__(self, memory_file='data/memory.json'):
        self.memory_file = memory_file
        self._init_memory()

    def _init_memory(self):
        if not os.path.exists('data'): os.makedirs('data')
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f: json.dump({"failures": []}, f)

    def calculate_compound_logic(self, balance):
        # الربح التراكمي: من 5 صفقات كحد أدنى إلى 20 كحد أقصى
        slots = max(5, min(int(balance / 11.0), 20))
        trade_amount = balance / slots
        return slots, trade_amount

    def analyze_momentum(self, ohlcv):
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        avg_vol = df['v'].tail(10).mean()
        curr_vol = df['v'].iloc[-1]
        # دخول عند زخم شراء قوي (سيولة أعلى بـ 30%)
        if curr_vol > (avg_vol * 1.3) and df['c'].iloc[-1] > df['o'].iloc[-1]:
            return "BUY_NOW"
        return "WAIT"
        
