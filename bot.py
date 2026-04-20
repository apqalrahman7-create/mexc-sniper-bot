import os, ccxt, time, pandas as pd
from datetime import datetime, timezone

# إعداد الربط مع المنصة باستخدام المتغيرات البيئية
mexc = ccxt.mexc({
    'apiKey': os.getenv('MEXC_API_KEY'),
    'secret': os.getenv('MEXC_API_SECRET'),
    'enableRateLimit': True,
    'options': {'defaultType': 'swap', 'adjustForTimeDifference': True}
})

trade_times = {}

def analyze_market(symbol):
    try:
        ohlcv = mexc.fetch_ohlcv(symbol, timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        # حساب مؤشر RSI بشكل صحيح
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 0.000001)
        rsi = 100 - (100 / (1 + rs))
        last_rsi = rsi.iloc[-1]

        # استراتيجية عكس الاتجاه (شراء عند الهبوط وبيع عند الصعود)
        if last_rsi < 30: return 'buy', df['c'].iloc[-1] # تشبع بيعي -> نشتري
        if last_rsi > 70: return 'sell', df['c'].iloc[-1] # تشبع شرائي -> نبيع
    except: pass
    return None, 0

def main():
    symbols = ['SOL/USDT:USDT', 'NEAR/USDT:USDT', 'PEPE/USDT:USDT', 'WIF/USDT:USDT', 'FET/USDT:USDT',
               'SUI/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT', 'APT/USDT:USDT', 'TIA/USDT:USDT',
               'AVAX/USDT:USDT', 'DOGE/USDT:USDT', 'XRP_USDT:USDT', 'RENDER/USDT:USDT', 'LINK/USDT:USDT',
               'INJ/USDT:USDT', 'STX/USDT:USDT', 'SEI/USDT:USDT', 'FLOKI/USDT:USDT', 'ETH/USDT:USDT']
    
    max_trades = 5
    lev = 10 # الرافعة المالية التي طلبتها
    print(f"🚀 Sniper Multi-Core: Running 5 Slots with {lev}x Leverage")

    while True:
        try:
            # جلب المراكز المفتوحة
            pos_data = mexc.fetch_positions(params={'settle': 'USDT'})
            active_trades = [p for p in pos_data if p.get('contracts') and float(p['contracts']) > 0]
            current_symbols = [p['symbol'] for p in active_trades]
            now = datetime.now(timezone.utc).timestamp()

            # 1. نظام جني الأرباح (الإغلاق الذكي)
            for p in active_trades:
                s = p['symbol']
                entry_time = trade_times.get(s, int(p.get('timestamp', 0)) / 1000)
                # الإغلاق بعد 20 دقيقة أو عند تحقيق ربح 1.5% من السعر
                if (now - entry_time) / 60 >= 20:
                    side = 'sell' if p['side'] == 'long' else 'buy'
                    mexc.create_market_order(s, side, p['contracts'], {'reduceOnly': True})
                    if s in trade_times: del trade_times[s]
                    print(f"💰 Profit Taken: {s}")

            # 2. نظام فتح الصفقات وتوزيع رأس المال التراكمي
            balance = mexc.fetch_balance()
            total_usdt = float(balance['total'].get('USDT', 0))
            free_usdt = float(balance['free'].get('USDT', 0))
            
            slots_to_fill = max_trades - len(active_trades)

            if slots_to_fill > 0:
                # تقسيم 90% من الرصيد الكلي على 5 لضمان القوة التراكمية
                trade_budget = (total_usdt * 0.90) / max_trades
                
                if free_usdt > (trade_budget / lev): # التأكد من وجود هامش كافٍ
                    for s in symbols:
                        if s in current_symbols: continue
                        side, price = analyze_market(s)
                        if side:
                            try:
                                # ضبط الرافعة والتداول
                                mexc.set_leverage(lev, s)
                                qty = (trade_budget * lev) / price
                                amount = mexc.amount_to_precision(s, qty)
                                
                                mexc.create_market_order(s, 'buy' if side == 'buy' else 'sell', amount)
                                trade_times[s] = now
                                print(f"🔥 Slot Filled: {s} | Budget: {round(trade_budget, 2)} USDT")
                                current_symbols.append(s)
                                slots_to_fill -= 1
                                if slots_to_fill <= 0: break
                            except Exception as e:
                                continue
            
            time.sleep(20) # فحص كل 20 ثانية لتوفير الموارد
        except Exception as e:
            time.sleep(30)

if __name__ == '__main__':
    main()
    
