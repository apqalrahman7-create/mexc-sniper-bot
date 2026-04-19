import streamlit as st
import ccxt
import time
from brain import AICore

# --- الإعدادات ---
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'ORDI/USDT:USDT',
    'SUI/USDT:USDT', 'XRP/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'LINK/USDT:USDT', 'AVAX/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT',
    'DOT/USDT:USDT', 'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'UNI/USDT:USDT',
    'APT/USDT:USDT', 'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT'
]
LEVERAGE = 5

st.set_page_config(page_title="MEXC AI Sniper Core", layout="wide")
st.title("🎯 MEXC AI Core - لوحة التحكم الذكية")

brain = AICore()

if 'running' not in st.session_state: st.session_state.running = False

# الجانب الجانبي للإعدادات
with st.sidebar:
    st.header("🔑 إعدادات الحساب")
    # محاولة جلب المفاتيح من النظام لسهولة الاستخدام
    api_key = st.text_input("API Key", value=st.secrets.get("API_KEY", ""), type="password")
    api_secret = st.text_input("Secret Key", value=st.secrets.get("API_SECRET", ""), type="password")
    
    if st.button("🚀 بدء التداول الآلي"): st.session_state.running = True
    if st.button("🛑 إيقاف النظام"): st.session_state.running = False

if st.session_state.running and api_key and api_secret:
    try:
        mexc = ccxt.mexc({
            'apiKey': api_key, 'secret': api_secret,
            'options': {'defaultType': 'swap'}, 'enableRateLimit': True
        })

        # أماكن عرض البيانات الحية
        bal_placeholder = st.empty()
        log_placeholder = st.container()

        while st.session_state.running:
            # 1. تحديث الرصيد والبيانات
            balance = mexc.fetch_balance()
            current_bal = float(balance['total']['USDT'])
            num_slots, trade_size = brain.calculate_position_size(current_bal)
            
            # جلب الصفقات الحالية
            pos = mexc.fetch_positions()
            active_p = [p['symbol'] for p in pos if float(p.get('contracts', 0)) != 0]
            
            bal_placeholder.info(f"💰 الرصيد التراكمي: {current_bal:.2f} USDT | الصفقات المفتوحة: {len(active_p)}/{num_slots}")

            for symbol in SYMBOLS:
                if len(active_p) >= num_slots: break 
                if symbol not in active_p:
                    ohlcv = mexc.fetch_ohlcv(symbol, timeframe='15m', limit=20)
                    decision = brain.analyze_momentum(ohlcv)
                    
                    if decision == "STRONG_MOMENTUM":
                        try:
                            # ضبط الرافعة 5x أولاً قبل الشراء
                            mexc.set_leverage(LEVERAGE, symbol)
                            
                            ticker = mexc.fetch_ticker(symbol)
                            qty = (trade_size * LEVERAGE) / ticker['last']
                            
                            mexc.create_market_order(symbol, 'buy', qty)
                            st.toast(f"✅ تم دخول صفقة ذكية: {symbol}", icon='🚀')
                            with log_placeholder:
                                st.write(f"🕒 {time.strftime('%H:%M:%S')} | تم شراء **{symbol}** بمبلغ {trade_size:.2f}$")
                            active_p.append(symbol)
                        except Exception as e:
                            continue
            
            time.sleep(30)
    except Exception as e:
        st.error(f"⚠️ خطأ في الاتصال: {e}")
        st.session_state.running = False

# نصيحة: إذا كنت ستستخدم هذا الكود على الهاتف، يفضل تركه مفتوحاً في المتصفح.
