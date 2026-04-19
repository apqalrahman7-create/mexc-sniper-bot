import ccxt
import config

class MexcExchange:
    def __init__(self):
        # الاتصال بالمنصة باستخدام المفاتيح من ملف config
        self.client = ccxt.mexc({
            'apiKey': config.API_KEY,
            'secret': config.API_SECRET,
            'options': {
                'defaultType': 'swap'  # تفعيل التداول الآجل (Futures)
            }
        })

    def get_total_balance(self):
        """جلب الرصيد الإجمالي المتاح في حساب الـ Futures"""
        try:
            balance = self.client.fetch_balance()
            return float(balance['total']['USDT'])
        except Exception as e:
            print(f"خطأ في جلب الرصيد: {e}")
            return config.INITIAL_BALANCE

    def setup_leverage(self, symbol):
        """ضبط الرافعة المالية لـ 5x لكل عملة قبل الدخول"""
        try:
            self.client.set_leverage(config.LEVERAGE, symbol)
        except Exception as e:
            # بعض العملات قد تكون الرافعة مضبوطة مسبقاً
            pass

    def fetch_market_data(self, symbol):
        """جلب بيانات شموع 15 دقيقة لتحليلها بواسطة الـ AI Core"""
        try:
            # جلب آخر 50 شمعة
            ohlcv = self.client.fetch_ohlcv(symbol, timeframe=config.TIMEFRAME, limit=50)
            return ohlcv
        except Exception as e:
            print(f"خطأ في جلب بيانات {symbol}: {e}")
            return None

    def execute_order(self, symbol, side, amount):
        """تنفيذ أمر بيع أو شراء"""
        try:
            # side: 'buy' أو 'sell'
            order = self.client.create_market_order(symbol, side, amount)
            print(f"تم تنفيذ صفقة {side} على {symbol} بنجاح.")
            return order
        except Exception as e:
            print(f"فشل في تنفيذ الصفقة: {e}")
            return None
          
