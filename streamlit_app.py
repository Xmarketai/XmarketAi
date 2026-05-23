import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="XmarketAi Master", layout="wide")

# 30+ TILLGÅNGAR
TICKERS = [
    "NVDA", "AMD", "AVGO", "INTC", "TSM", "ARM", "MU", "QCOM", 
    "RKLB", "TSLA", "PLTR", "ASTS", "SPCE", "LMT", "BA",
    "VST", "CEG", "OKLO", "VRT", "NEE", "GEV", "XOM",
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOT-USD",
    "MSFT", "GOOGL", "AMZN", "META", "ORCL", "SNOW"
]

st.title("⚡ XmarketAi: Master Engine")

# HÄMTA DATA - Batchat för att undvika fel
@st.cache_data(ttl=60)
def fetch_data(tickers):
    data = yf.Tickers(" ".join(tickers))
    results = {}
    for t in tickers:
        try:
            info = data.tickers[t].info
            results[t] = info.get('regularMarketPrice') or info.get('currentPrice') or 0.0
        except:
            results[t] = 0.0
    return results

prices = fetch_data(TICKERS)

# ENKEL GRID-LAYOUT - Inga komplexa komponenter som kraschar
cols = st.columns(6)
for i, ticker in enumerate(TICKERS):
    with cols[i % 6]:
        price = prices.get(ticker, 0)
        st.metric(ticker, f"{price:,.2f}")
        # Knapp för analys som INTE laddar om hela sidan
        if st.button("Analysera", key=f"btn_{ticker}"):
            st.write(f"Klar för analys av {ticker} (Pris: {price})")

st.info("Systemet laddat. Om du ser tomma rutor, uppdatera sidan.")
        except:
            st.write(f"{ticker}: Väntar...")
