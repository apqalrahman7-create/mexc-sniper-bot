import os

# الأمان: جلب المفاتيح من النظام
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')

# إعدادات الاستراتيجية
LEVERAGE = 5
INITIAL_BALANCE = 56.0
MIN_TRADE_SIZE = 11.0  # لضمان الربح التراكمي وتوزيع المخاطر
TIMEFRAME = '15m'

# قائمة الـ 20 عملة
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'ORDI/USDT:USDT',
    'SUI/USDT:USDT', 'XRP/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'LINK/USDT:USDT', 'AVAX/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT',
    'DOT/USDT:USDT', 'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'UNI/USDT:USDT',
    'APT/USDT:USDT', 'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT'
]

MEMORY_FILE = "data/memory.json"
