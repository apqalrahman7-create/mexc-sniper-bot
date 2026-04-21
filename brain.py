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
        # تعديل: 3 صفقات فقط لتركيز الميزانية (الربح التراكمي)
        slots = 3 
        # نستخدم 98% من الرصيد لضمان دخول قوي جداً مع نظام Cross
        trade_margin = (current_balance * 0.98) / slots
        return slots, trade_margin

    def analyze_momentum(self, ohlcv):
        """الاستراتيجية المطلوبة: أحمر = شراء | أخضر = بيع"""
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        
        # جلب بيانات آخر شمعة مكتملة
        last_open = df['o'].iloc[-1]
        last_close = df['c'].iloc[-1]
        
        # إذا كانت الشمعة حمراء (إغلاق أقل من افتتاح) -> نشتري Long
        if last_close < last_open:
            return "BUY_SIGNAL"
        
        # إذا كانت الشمعة خضراء (إغلاق أعلى من افتتاح) -> نبيع Short
        if last_close > last_open:
            return "SELL_SIGNAL"
            
        return "WAIT"
        
