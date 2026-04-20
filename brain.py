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
        # تعديل: نركز القوة في 5 صفقات فقط لتعظيم الربح التراكمي
        slots = 5 
        # نستخدم 95% من الرصيد لضمان دخول قوي مع ترك هامش بسيط للرسوم
        trade_margin = (current_balance * 0.95) / slots
        return slots, trade_margin

    def analyze_momentum(self, ohlcv):
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        
        # مؤشرات سريعة للسكالبينج (تغير السعر في آخر 3 دقائق)
        last_prices = df['c'].tail(3).tolist()
        
        # شرط دخول أكثر مرونة: إذا كان هناك صعود مستمر في آخر 3 شموع
        if last_prices[-1] > last_prices[-2] > last_prices[-3]:
            return "BUY_SIGNAL"
        
        # شرط بيع (Short): إذا كان هناك هبوط مستمر
        if last_prices[-1] < last_prices[-2] < last_prices[-3]:
            return "SELL_SIGNAL"
            
        return "WAIT"
        
