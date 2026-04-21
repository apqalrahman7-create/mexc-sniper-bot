import os

# الأمان (سيتم جلبها من المتغيرات البيئية أو إدخالها يدوياً)
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')

# إعدادات القوة القصوى والربح التراكمي لعام 2026
LEVERAGE = 20           # رفع الرافعة لـ 20x لتعظيم الربح من الـ 40 دولار
MARGIN_MODE = 'CROSS'   # تفعيل الهامش المتبادل كما طلبت
INITIAL_BALANCE = 41.0  # تحديث الرصيد الحالي
MIN_TRADE_SIZE = 7.5    # الحد الأدنى للصفقة في MEXC عقود
TIMEFRAME = '1m'        # مراقبة الشموع كل دقيقة (أحمر شراء | أخضر بيع)

# قائمة 20 عملة (تم حذف BTC وإضافة عملات قوية وسريعة)
SYMBOLS = [
    'ETH/USDT:USDT', 'SOL/USDT:USDT', 'ORDI/USDT:USDT', 'SUI/USDT:USDT',
    'XRP/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT', 'LINK/USDT:USDT',
    'AVAX/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT', 'DOT/USDT:USDT',
    'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'UNI/USDT:USDT', 'APT/USDT:USDT',
    'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT', 'PEPE/USDT:USDT'
]

MEMORY_FILE = "data/memory.json"
