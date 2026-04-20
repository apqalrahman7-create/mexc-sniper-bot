cat <<EOF > start.py
import os, ccxt, time, pandas as pd
from datetime import datetime, timezone

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
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / (loss + 0.000001))))
        last_rsi = rsi.iloc[-1]
        if last_rsi > 65: return 'buy', df['c'].iloc[-1]
        if last_rsi < 35: return 'sell', df['c'].iloc[-1]
    except: pass
    return None, 0

def main():
    symbols = ['SOL/USDT:USDT', 'NEAR/USDT:USDT', 'PEPE/USDT:USDT', 'WIF/USDT:USDT', 'FET/USDT:USDT',
               'SUI/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT', 'APT/USDT:USDT', 'TIA/USDT:USDT',
               'AVAX/USDT:USDT', 'DOGE/USDT:USDT', 'XRP/USDT:USDT', 'RENDER/USDT:USDT', 'LINK/USDT:USDT',
               'INJ/USDT:USDT', 'STX/USDT:USDT', 'SEI/USDT:USDT', 'FLOKI/USDT:USDT', 'ETH/USDT:USDT']
    
    max_trades = 5
    print("🚀 Sniper Multi-Core: Cleaning Warehouse & Starting 5 Slots")

    while True:
        try:
            pos_data = mexc.fetch_positions(params={'settle': 'USDT'})
            active_trades = [p for p in pos_data if p.get('contracts') and float(p['contracts']) > 0]
            current_symbols = [p['symbol'] for p in active_trades]
            now = datetime.now(timezone.utc).timestamp()

            # إغلاق الصفقات (بعد 20 دقيقة)
            for p in active_trades:
                s = p['symbol']
                pnl = float(p.get('unrealizedPnl', 0) or 0)
                entry_time = trade_times.get(s, int(p.get('timestamp', 0)) / 1000)
                if (now - entry_time) / 60 >= 20 or pnl >= 2.0:
                    mexc.create_market_order(s, 'sell' if p['side'] == 'long' else 'buy', p['contracts'], {'reduceOnly': True})
                    if s in trade_times: del trade_times[s]

            # فتح حتى 5 صفقات متنوعة
            balance = mexc.fetch_balance()
            free_usdt = float(balance['total'].get('USDT', 0)) if len(active_trades) == 0 else float(balance['free'].get('USDT', 0))
            slots_to_fill = max_trades - len(active_trades)

            if slots_to_fill > 0 and free_usdt > 10:
                trade_budget = (free_usdt * 0.90) / slots_to_fill
                for s in symbols:
                    if s in current_symbols: continue
                    side, price = analyze_market(s)
                    if side:
                        try:
                            mexc.set_leverage(20, s)
                            qty = (trade_budget * 20) / price
                            mexc.create_market_order(s, side, mexc.amount_to_precision(s, qty))
                            trade_times[s] = now
                            print(f"🔥 Slot Filled: {s}")
                            current_symbols.append(s)
                            slots_to_fill -= 1
                            if slots_to_fill <= 0: break
                        except: continue
            time.sleep(15)
        except Exception as e:
            time.sleep(20)

if __name__ == '__main__':
    main()
EOF
