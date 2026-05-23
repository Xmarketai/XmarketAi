import streamlit as st
import yfinance as yf
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="XmarketAi Live", layout="wide")
st.markdown("<style>.block-container { max-width: 98% !important; }</style>", unsafe_allow_html=True)

# 2. FULLSTÄNDIG TILLGÅNGSLISTA (30+ tillgångar)
TICKERS = {
    "AI/Semis": ["NVDA", "AMD", "AVGO", "INTC", "TSM", "ARM"],
    "Space/Future": ["RKLB", "TSLA", "PLTR", "ASTS", "SPCE"],
    "Energy": ["VST", "CEG", "OKLO", "VRT", "NEE"],
    "Crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
    "AGI/Cloud": ["MSFT", "GOOGL", "AMZN", "META", "ORCL"]
}

st.title("⚡ XmarketAi: Live Command Center")

# 3. LIVE-HÄMTNINGS-FUNKTION
@st.cache_data(ttl=60) # Cachear data i 60 sekunder för att inte bli spärrad
def get_live_data(tickers):
    data = yf.Tickers(" ".join(tickers))
    results = {}
    for t in tickers:
        try:
            info = data.tickers[t].info
            results[t] = info.get('regularMarketPrice') or info.get('currentPrice')
        except:
            results[t] = 0.0
    return results

# 4. RENDERING
tabs = st.tabs(list(TICKERS.keys()))

for i, cat in enumerate(TICKERS.keys()):
    with tabs[i]:
        prices = get_live_data(TICKERS[cat])
        cols = st.columns(4)
        for j, ticker in enumerate(TICKERS[cat]):
            with cols[j % 4]:
                price = prices.get(ticker, "N/A")
                st.metric(ticker, f"{price:,.2f} USD")

# 5. SIDEBAR: Live-status
with st.sidebar:
    st.header("System Status")
    st.success("Live-data från Yahoo Finance")
    if st.button("Uppdatera nu"):
        st.cache_data.clear()
        st.rerun()
