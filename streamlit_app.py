import streamlit as st
import yfinance as yf
import pandas as pd
import anthropic

st.set_page_config(page_title="XmarketAi Master Engine", layout="wide")

# CSS för att eliminera allt "luft" och tvinga fram en tät, professionell vy
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 99% !important; }
    .stMetric { background-color: #0e1117; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    div[data-testid="stMetricValue"] { font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

# 30+ TILLGÅNGAR - FULL LISTA
TICKERS = [
    "NVDA", "AMD", "AVGO", "INTC", "TSM", "ARM", "MU", "QCOM", # AI/Chips
    "RKLB", "TSLA", "PLTR", "ASTS", "SPCE", "LMT", "BA",        # Space/Tech
    "VST", "CEG", "OKLO", "VRT", "NEE", "GEV", "XOM",          # Energy
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOT-USD",      # Crypto
    "MSFT", "GOOGL", "AMZN", "META", "ORCL", "SNOW"             # AGI/Cloud
]

st.title("⚡ XmarketAi: Master Command Center")

# API NYCKEL (Alltid tillgänglig i sidebar)
with st.sidebar:
    st.header("🔑 Anthropic API")
    api_key = st.text_input("Claude Key:", type="password")
    st.write("---")
    st.write("Status: Live-data")

# HÄMTA ALL DATA I EN BATCH (Mycket snabbare & stabilare)
data = yf.Tickers(" ".join(TICKERS))

# GRID-VY FÖR ALLA 30+
# Vi ritar upp 6 kolumner för att få plats med allt på en skärm
cols = st.columns(6)

for i, ticker in enumerate(TICKERS):
    col = cols[i % 6]
    with col:
        try:
            info = data.tickers[ticker].info
            price = info.get('regularMarketPrice') or info.get('currentPrice')
            
            with st.container():
                st.metric(ticker, f"{price:,.2f}")
                if st.button("Analys", key=f"btn_{ticker}"):
                    if api_key:
                        client = anthropic.Anthropic(api_key=api_key)
                        msg = client.messages.create(
                            model="claude-3-5-sonnet-20240620",
                            max_tokens=150,
                            messages=[{"role": "user", "content": f"Snabb analys av {ticker} vid pris {price}"}]
                        )
                        st.sidebar.info(f"Analys {ticker}: {msg.content[0].text}")
                    else:
                        st.sidebar.error("Ingen API-nyckel")
        except:
            st.write(f"{ticker}: Väntar...")
