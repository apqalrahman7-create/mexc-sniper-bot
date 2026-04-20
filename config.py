import os

# الأمان
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')

# إعدادات مطورة للتطور والربح التراكمي
LEVERAGE = 10           # رفع الرافعة لـ 10 كما طلبت لزيادة القوة
INITIAL_BALANCE = 56.0  
MIN_TRADE_SIZE = 5.0    # تقليل الحد الأدنى للسماح بفتح 5 صفقات دائماً
TIMEFRAME = '1m'        # تغيير الوقت لـ 1 دقيقة لمراقبة الإغلاق بدقة

# قائمة العملات (تم الإبقاء عليها كما هي)
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'ORDI/USDT:USDT',
    'SUI/USDT:USDT', 'XRP/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'LINK/USDT:USDT', 'AVAX/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT',
    'DOT/USDT:USDT', 'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'UNI/USDT:USDT',
    'APT/USDT:USDT', 'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT'
]

MEMORY_FILE = "data/memory.json"
