import os, ccxt, time, pandas as pd
from datetime import datetime, timezone

# إدخال المفاتيح عند التشغيل
API_KEY = input("Enter NEW API KEY: ")
SECRET_KEY = input("Enter NEW SECRET KEY: ")

# إعداد الربط مع المنصة (نظام كسر الحظر)
mexc = ccxt.mexc({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'swap', 
        'adjustForTimeDifference': True,
        'headers': {'User-Agent': 'Mozilla/5.0'}
    }
})

def analyze_market(symbol):
    """تحليل الشموع: إغلاق < افتتاح = أحمر (شراء) | إغلاق > افتتاح = أخضر (بيع)"""
    try:
        ohlcv = mexc.fetch_ohlcv(symbol, timeframe='1m', limit=2)
        last_candle = ohlcv[-1]
        open_p, close_p = last_candle[1], last_candle[4]
        
        if close_p < open_p: return 'buy', close_p   # شمعة حمراء -> شراء Long
        if close_p > open_p: return 'sell', close_p  # شمعة خضراء -> بيع Short
    except: pass
    return None, 0

def main():
    symbols = ['SOL/USDT:USDT', 'NEAR/USDT:USDT', 'PEPE/USDT:USDT', 'WIF/USDT:USDT', 'FET/USDT:USDT',
               'SUI/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT', 'APT/USDT:USDT', 'TIA/USDT:USDT',
               'AVAX/USDT:USDT', 'DOGE/USDT:USDT', 'XRP/USDT:USDT', 'RENDER/USDT:USDT', 'LINK/USDT:USDT',
               'INJ/USDT:USDT', 'STX/USDT:USDT', 'SEI/USDT:USDT', 'FLOKI/USDT:USDT', 'ETH/USDT:USDT']
    
    max_trades = 3 # 3 صفقات متزامنة لتركيز القوة
    lev = 20 # رافعة 20x
    print(f"🚀 Sniper Active | Red=Long, Green=Short | 20x Leverage | Cross Margin")

    while True:
        try:
            # 1. فحص المراكز المفتوحة
            pos = mexc.fetch_positions(params={'settle': 'USDT'})
            active = [p for p in pos if float(p.get('contracts', 0)) > 0]
            current_symbols = [p['symbol'] for p in active]

            # 2. فتح صفقات جديدة (ربح تراكمي)
            if len(active) < max_trades:
                bal = mexc.fetch_balance()
                total_usdt = float(bal['total'].get('USDT', 0))
                # تقسيم 90% من الرصيد على عدد الصفقات المتاحة
                trade_budget = (total_usdt * 0.90) / max_trades 

                for s in symbols:
                    if s in current_symbols: continue
                    if len(active) >= max_trades: break
                    
                    side, price = analyze_market(s)
                    if side:
                        try:
                            # ضبط الهامش المتبادل والرافعة
                            try: mexc.set_margin_mode('CROSS', s)
                            except: pass
                            mexc.set_leverage(lev, s)
                            
                            qty = (trade_budget * lev) / price
                            amount = mexc.amount_to_precision(s, qty)
                            
                            mexc.create_market_order(s, 'buy' if side == 'buy' else 'sell', amount)
                            print(f"🔥 {'🔴 BUY' if side=='buy' else '🟢 SELL'} {s} | Amount: {round(trade_budget, 2)}$")
                            active.append(s) # تحديث القائمة مؤقتاً
                        except: continue
            
            time.sleep(15) # فحص كل 15 ثانية
        except Exception as e:
            time.sleep(10)

if __name__ == '__main__':
    main()
    
