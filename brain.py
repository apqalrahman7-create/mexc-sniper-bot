import json
import os
import pandas as pd

class AICore:
    def __init__(self, memory_file='data/memory.json'):
        self.memory_file = memory_file
        self.ensure_memory_exists()

    def ensure_memory_exists(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({"failed_patterns": [], "history": []}, f)

    def calculate_position_size(self, current_balance):
        # تقسيم الرصيد لضمان الربح التراكمي (بين 5 إلى 20 صفقة)
        min_trade_size = 11.0
        slots = max(5, min(int(current_balance / min_trade_size), 20))
        return slots, (current_balance / slots)

    def analyze_momentum(self, ohlcv):
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        avg_v = df['v'].tail(10).mean()
        curr_v = df['v'].iloc[-1]
        # إذا كان حجم التداول الحالي أكبر من المتوسط بـ 30% والسعر صاعد
        if curr_v > (avg_v * 1.3) and df['c'].iloc[-1] > df['o'].iloc[-1]:
            return "BUY_SIGNAL"
        return "WAIT"
      
