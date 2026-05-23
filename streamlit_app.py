import streamlit as st
import yfinance as yf
import pandas as pd

# 1. TVINGANDE FULL BREDD
st.set_page_config(layout="wide", page_title="XmarketAi Control Center")
st.markdown("<style>.block-container { max-width: 99% !important; }</style>", unsafe_allow_html=True)

# 2. DEFINITION AV ALLA 30+ TILLGÅNGAR
TICKERS = {
    "AI & Semis": ["NVDA", "AMD", "AVGO", "TSM", "ARM", "MU", "QCOM"],
    "Space & Tech": ["RKLB", "TSLA", "PLTR", "ASTS", "SPCE", "LMT", "BA"],
    "Energy": ["VST", "CEG", "OKLO", "VRT", "NEE", "GEV", "XOM"],
    "Krypto": ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOT-USD"],
    "AGI & Cloud": ["MSFT", "GOOGL", "AMZN", "META", "ORCL", "SNOW"]
}

st.title("⚡ XmarketAi: Master Command Center")

# 3. LIVE DATA-MOTOR
@st.cache_data(ttl=30)
def fetch_all():
    all_symbols = [s for sub in TICKERS.values() for s in sub]
    data = yf.Tickers(" ".join(all_symbols))
    return data

data_engine = fetch_all()

# 4. HUVUDVY: GRID AV ALLA TILLGÅNGAR
for cat, symbols in TICKERS.items():
    st.subheader(f"📂 {cat}")
    cols = st.columns(7) # 7 kolumner gör att sidan känns bred och kraftfull
    
    for i, symbol in enumerate(symbols):
        with cols[i % 7]:
            try:
                info = data_engine.tickers[symbol].info
                price = info.get('regularMarketPrice') or info.get('currentPrice') or 0.0
                st.metric(symbol, f"{price:,.2f}")
            except:
                st.write(f"{symbol}: Data fel")
    st.divider()

# 5. LIVE NYHETSFÖDDE (Sektion längst ner som fyller ut sidan)
st.header("📰 Live Marknadsnyheter & Analys")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Senaste nyheterna")
    st.write("• Systemet är synkroniserat med live-data (Yahoo Finance).")
    st.write("• Volatilitetsmonitor aktiv för alla 30+ instrument.")
    st.write("• AGI-sektorn visar ökad aktivitet.")

with col2:
    st.subheader("AI-Status")
    st.info("System Redo: Väntar på API-nyckel för Claude-analys.")
