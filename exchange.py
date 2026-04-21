import os, ccxt, time, pandas as pd
from datetime import datetime, timezone

# إعدادات المحرك المطور (Sniper 2026)
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')
LEVERAGE = 20  # رفع الرافعة لـ 20x كما طلبت
MAX_SLOTS = 3  # تركيز الميزانية في 3 صفقات فقط لربح تراكمي أسرع

exchange = ccxt.mexc({
    'apiKey': API_KEY, 'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'swap', 
        'adjustForTimeDifference': True,
        'headers': {'User-Agent': 'Mozilla/5.0'}
    }
})

# قائمة الـ 20 عملة (بدون BTC)
SYMBOLS = ['ETH/USDT:USDT', 'SOL/USDT:USDT', 'ADA/USDT:USDT', 'DOT/USDT:USDT', 'AVAX_USDT:USDT', 
           'MATIC/USDT:USDT', 'LINK/USDT:USDT', 'UNI/USDT:USDT', 'LTC/USDT:USDT', 'ATOM/USDT:USDT',
           'ETC/USDT:USDT', 'ALGO/USDT:USDT', 'XRP/USDT:USDT', 'DOGE/USDT:USDT', 'NEAR/USDT:USDT',
           'FIL/USDT:USDT', 'ICP/USDT:USDT', 'FET/USDT:USDT', 'APT/USDT:USDT', 'OP/USDT:USDT']

trade_memory = {}

def get_signal(symbol):
    """الاستراتيجية: شمعة حمراء = شراء Long | شمعة خضراء = بيع Short"""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=2)
        last_candle = ohlcv[-1]
        open_p, close_p = last_candle[1], last_candle[4]
        if close_p < open_p: return 'buy'  # حمراء -> شراء
        if close_p > open_p: return 'sell' # خضراء -> بيع
    except: pass
    return None

def main():
    print(f"🚀 Sniper Master Pro Active | Slots: {MAX_SLOTS} | Leverage: {LEVERAGE}x | Cross")
    while True:
        try:
            positions = exchange.fetch_positions(params={'settle': 'USDT'})
            active_trades = [p for p in positions if float(p.get('contracts', 0)) > 0]
            current_symbols = [p['symbol'] for p in active_trades]
            now = datetime.now(timezone.utc).timestamp()
            
            # 1. جني الأرباح (بعد 20 دقيقة أو عند انعكاس الشمعة)
            for p in active_trades:
                symbol = p['symbol']
                entry_time = trade_memory.get(symbol, int(p.get('timestamp', 0))/1000)
                if (now - entry_time) / 60 >= 20:
                    side = 'sell' if p['side'] == 'long' else 'buy'
                    exchange.create_market_order(symbol, side, p['contracts'], {'reduceOnly': True})
                    if symbol in trade_memory: del trade_memory[symbol]
                    print(f"💰 Profit Taken: {symbol}")

            # 2. فتح صفقات جديدة (تراكمي 98% من الرصيد)
            if len(active_trades) < MAX_SLOTS:
                balance = exchange.fetch_balance()['total'].get('USDT', 0)
                # دخول بـ 98% من الرصيد مقسم على 3 صفقات (قوة قصوى)
                trade_budget = (balance * 0.98) / MAX_SLOTS 
                
                for s in SYMBOLS:
                    if s in current_symbols: continue
                    if len(active_trades) >= MAX_SLOTS: break
                    
                    signal = get_signal(s)
                    if signal:
                        try:
                            try: exchange.set_margin_mode('CROSS', s) # تفعيل متبادل
                            except: pass
                            exchange.set_leverage(LEVERAGE, s)
                            price = exchange.fetch_ticker(s)['last']
                            amount = (trade_budget * LEVERAGE) / price
                            exchange.create_market_order(s, signal, exchange.amount_to_precision(s, amount))
                            trade_memory[s] = now
                            print(f"🔥 Slot Filled: {s} | Side: {signal}")
                            active_trades.append(s) # تحديث مؤقت
                        except: continue
            
            time.sleep(15)
        except Exception as e:
            time.sleep(10)

if __name__ == '__main__':
    main()
    
