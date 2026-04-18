import streamlit as st
import ccxt
import pandas as pd
import time
from datetime import datetime

# --- 🚀 إعدادات القناص العالمي (تراكمي) ---
SYMBOLS = ['ORDI_USDT', 'BTC_USDT', 'ETH_USDT', 'SOL_USDT', 'SUI_USDT', 'XRP_USDT']
MAX_TRADES = 4
LEVERAGE = 5
RISK_PERCENT = 0.15  # يستخدم 15% من الرصيد لكل صفقة لنمو تراكمي

st.set_page_config(page_title="MEXC Global Sniper", layout="wide")
st.title("🎯 قناص MEXC العالمي - نسخة الهاتف")

if 'running' not in st.session_state: st.session_state.running = False

with st.sidebar:
    st.header("🔑 Credentials")
    api_key = st.text_input("API Key", type="password")
    api_secret = st.text_input("Secret Key", type="password")
    if st.button("🚀 تشغيل المحرك"): st.session_state.running = True
    if st.button("🛑 إيقاف"): st.session_state.running = False

if st.session_state.running and api_key and api_secret:
    try:
        # الاتصال بنظام الـ Swap (العقود الآجلة في MEXC)
        mexc = ccxt.mexc({
            'apiKey': api_key, 'secret': api_secret,
            'options': {'defaultType': 'swap'}, 'enableRateLimit': True
        })

        while st.session_state.running:
            # جلب الرصيد والصفقات
            balance = mexc.fetch_balance()
            try:
                available_bal = float(balance['info']['data']['availableBalance'])
            except:
                available_bal = float(balance['USDT']['free'])

            pos = mexc.fetch_positions()
            active_p = [p['symbol'] for p in pos if float(p.get('contracts', 0)) != 0]
            current_count = len(active_p)
            
            st.write(f"💰 الرصيد: **{available_bal:.2f} USDT** | صفقات نشطة: {current_count}/4")

            for symbol in SYMBOLS:
                if current_count >= MAX_TRADES: break 
                
                if symbol not in active_p:
                    try:
                        ticker = mexc.fetch_ticker(symbol)
                        price = ticker['last']
                        
                        # حساب الحجم التراكمي
                        trade_value = available_bal * RISK_PERCENT
                        qty = (trade_value * LEVERAGE) / price
                        
                        mexc.create_market_order(symbol, 'buy', qty)
                        st.success(f"🚀 تم فتح صفقة {symbol} بمبلغ {trade_value:.2f}$")
                        current_count += 1
                        active_p.append(symbol) 
                    except: continue
            time.sleep(20)
    except Exception as e:
        st.error(f"⚠️ خطأ اتصال: {str(e)}")
        time.sleep(10)
      
