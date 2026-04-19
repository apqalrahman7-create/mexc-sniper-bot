# config.py - إعدادات البوت الذكي لـ MEXC
import os

# بيانات المنصة (استبدلها بمفاتيحك الحقيقية)
API_KEY = "ضـع_مـفـتـاحـك_هـنـا"
API_SECRET = "ضـع_الـسـر_هـنـا"

# إعدادات الميزانية الأساسية
INITIAL_BALANCE = 56.0  # الرصيد الأولي
LEVERAGE = 5            # الرافعة المالية الثابتة 5x

# إعدادات المرونة والربح التراكمي
# البوت سيحاول تخصيص حوالي 11$ لكل صفقة (لتغطية الحد الأدنى للمنصة)
MIN_USDT_PER_TRADE = 11.0 
MAX_TRADES_LIMIT = 20     # أقصى عدد صفقات يصل إليه عند زيادة الرصيد
MIN_TRADES_LIMIT = 5      # أقل عدد صفقات يفتحها بالرصيد الحالي

# إعدادات الوقت والعملات
TIMEFRAME = '15m'         # تحليل شمعة الـ 15 دقيقة
# قائمة بـ 20 عملة مقترحة (يمكنك تعديلها)
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'BNB/USDT:USDT',
    'AVAX/USDT:USDT', 'ADA/USDT:USDT', 'XRP/USDT:USDT', 'DOT/USDT:USDT',
    'LINK/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT', 'LTC/USDT:USDT',
    'ATOM/USDT:USDT', 'UNI/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'APT/USDT:USDT', 'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT'
]

# مسارات البيانات
MEMORY_FILE = "data/memory.json"
