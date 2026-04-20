import os, ccxt, time, pandas as pd
from datetime import datetime, timezone

# إعدادات المحرك (دمج Config و Exchange)
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')
LEVERAGE = 10
MAX_SLOTS = 5

exchange = ccxt.mexc({
    'apiKey': API_KEY, 'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'swap', 'adjustForTimeDifference': True}
})

SYMBOLS = ['SOL/USDT:USDT', 'NEAR/USDT:USDT', 'PEPE/USDT:USDT', 'WIF/USDT:USDT', 'SUI/USDT:USDT', 
           'OP/USDT:USDT', 'ARB/USDT:USDT', 'TIA/USDT:USDT', 'AVAX/USDT:USDT', 'ORDI/USDT:USDT']

trade_memory = {}

def get_signal(symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=30)
        df = pd.DataFrame(ohlcv, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        # تحليل الزخم السريع (آخر 3 شموع)
        if df['c'].iloc[-1] > df['c'].iloc[-2] > df['c'].iloc[-3]: return 'buy'
        if df['c'].iloc[-1] < df['c'].iloc[-2] < df['c'].iloc[-3]: return 'sell'
    except: pass
    return None

def main():
    print(f"🚀 Master Sniper Started | Slots: {MAX_SLOTS} | Leverage: {LEVERAGE}x")
    while True:
        try:
            # 1. جلب المراكز المفتوحة وجني الأرباح
            positions = exchange.fetch_positions(params={'settle': 'USDT'})
            active_trades = [p for p in positions if float(p.get('contracts', 0)) > 0]
            
            for p in active_trades:
                symbol = p['symbol']
                entry_time = trade_memory.get(symbol, int(p['timestamp'])/1000)
                # إغلاق بعد 20 دقيقة لضمان تدوير الربح التراكمي
                if (datetime.now(timezone.utc).timestamp() - entry_time) / 60 >= 20:
                    side = 'sell' if p['side'] == 'long' else 'buy'
                    exchange.create_market_order(symbol, side, p['contracts'], {'reduceOnly': True})
                    if symbol in trade_memory: del trade_memory[symbol]
                    print(f"💰 Closed & Profit Taken: {symbol}")

            # 2. فتح صفقات جديدة (تطوير تراكمي)
            if len(active_trades) < MAX_SLOTS:
                balance = exchange.fetch_balance()['total'].get('USDT', 0)
                trade_budget = (balance * 0.9) / MAX_SLOTS # تخصيص الرصيد بالعدل
                
                for s in SYMBOLS:
                    if s not in [p['symbol'] for p in active_trades]:
                        signal = get_signal(s)
                        if signal:
                            exchange.set_leverage(LEVERAGE, s)
                            price = exchange.fetch_ticker(s)['last']
                            amount = (trade_budget * LEVERAGE) / price
                            exchange.create_market_order(s, signal, exchange.amount_to_precision(s, amount))
                            trade_memory[s] = datetime.now(timezone.utc).timestamp()
                            print(f"🔥 Slot Filled: {s} | Budget: {round(trade_budget, 2)} USDT")
                            if len(active_trades) >= MAX_SLOTS: break
            
            time.sleep(20)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    main()
    
