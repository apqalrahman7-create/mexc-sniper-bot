import streamlit as st
import ccxt
import pandas as pd
import time
import json
import os
from brain import AICore  # استدعاء العقل الذي برمجناه

# --- 🚀 الإعدادات الذكية ---
# أضفنا 20 عملة كما طلبت ليتداول عليها البوت عند توفر السيولة
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'ORDI/USDT:USDT',
    'SUI/USDT:USDT', 'XRP/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'LINK/USDT:USDT', 'AVAX/USDT:USDT', 'MATIC/USDT:USDT', 'NEAR/USDT:USDT',
    'DOT/USDT:USDT', 'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'UNI/USDT:USDT',
    'APT/USDT:USDT', 'FIL/USDT:USDT', 'VET/USDT:USDT', 'INJ/USDT:USDT'
]
LEVERAGE = 5

st.set_page_config(page_title="MEXC AI Sniper Core", layout="wide")
st.title("🎯 MEXC AI Core - نظام التداول الذكي")

# تفعيل عقل البوت
brain = AICore()

if 'running' not in st.session_state: st.session_state.running = False

with st.sidebar:
    st.header("🔑 إعدادات الوصول")
    api_key = st.text_input("API Key", type="password")
    api_secret = st.text_input("Secret Key", type="password")
    if st.button("🚀 تشغيل المحرك الذكي"): st.session_state.running = True
    if st.button("🛑 إيقاف"): st.session_state.running = False

if st.session_state.running and api_key and api_secret:
    try:
        mexc = ccxt.mexc({
            'apiKey': api_key, 'secret': api_secret,
            'options': {'defaultType': 'swap'}, 'enableRateLimit': True
        })

        col1, col2 = st.columns(2)
        with col1: balance_area = st.empty()
        with col2: stats_area = st.empty()
        log_area = st.container()

        while st.session_state.running:
            # 1. جلب الرصيد الحقيقي للربح التراكمي
            balance = mexc.fetch_balance()
            current_bal = float(balance['total']['USDT'])
            
            # 2. حساب عدد الصفقات وحجمها ديناميكياً (AI Decision)
            num_slots, trade_size = brain.calculate_position_size(current_bal)
            
            # 3. جلب الصفقات المفتوحة حالياً
            pos = mexc.fetch_positions()
            active_p = [p['symbol'] for p in pos if float(p.get('contracts', 0)) != 0]
            
            balance_area.metric("الرصيد الإجمالي (تراكمي)", f"{current_bal:.2f} USDT")
            stats_area.write(f"📊 الحد الأقصى للصفقات حالياً: **{num_slots}** | نشط: {len(active_p)}")

            for symbol in SYMBOLS:
                if len(active_p) >= num_slots: break 
                
                if symbol not in active_p:
                    # جلب البيانات لتحليل السيولة (Momentum)
                    ohlcv = mexc.fetch_ohlcv(symbol, timeframe='15m', limit=20)
                    
                    # قرار الـ AI: فحص السيولة + فحص الذاكرة لمنع الفشل
                    decision = brain.analyze_momentum(ohlcv)
                    is_safe = brain.is_learning_from_failure(symbol, "MOMENTUM_CHECK")

                    if decision == "STRONG_MOMENTUM" and is_safe:
                        try:
                            ticker = mexc.fetch_ticker(symbol)
                            price = ticker['last']
                            
                            # حساب الكمية بناءً على الرافعة 5x
                            qty = (trade_size * LEVERAGE) / price
                            
                            mexc.create_market_order(symbol, 'buy', qty)
                            with log_area:
                                st.success(f"✅ {symbol}: دخول ذكي بمبلغ {trade_size:.2f}$")
                            active_p.append(symbol)
                        except Exception as e:
                            brain.record_failure(symbol, "EXECUTION_ERROR", str(e))
                            continue
            
            time.sleep(30) # انتظار نصف دقيقة قبل الفحص التالي
    except Exception as e:
        st.error(f"⚠️ خطأ: {str(e)}")
        time.sleep(10)
        
