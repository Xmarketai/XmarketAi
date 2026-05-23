import streamlit as st
import yfinance as yf
import pandas as pd
import anthropic

st.set_page_config(page_title="XmarketAi Master Engine", layout="wide")

# DEFINITION AV ALLA 30+ TILLGÅNGAR
TILLGANGAR = {
    "AI & Semis": ["NVDA", "AMD", "AVGO", "INTC", "TSM", "ARM", "MU", "QCOM"],
    "Space & Tech": ["RKLB", "TSLA", "PLTR", "ASTS", "SPCE", "LMT", "BA"],
    "Energy": ["VST", "CEG", "OKLO", "VRT", "NEE", "GEV", "XOM"],
    "Krypto": ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOT-USD"],
    "AGI & Cloud": ["MSFT", "GOOGL", "AMZN", "META", "ORCL", "SNOW", "CRM"]
}

st.title("⚡ XmarketAi: Fullständig Master Engine")

# Sidomeny för API
with st.sidebar:
    api_key = st.text_input("Claude API Nyckel:", type="password")

# LOOPA IGENOM ALLA KATEGORIER OCH TILLGÅNGAR
for kategori, tickers in TILLGANGAR.items():
    st.subheader(f"📂 {kategori}")
    # Skapa kolumner för varje rad
    cols = st.columns(4)
    
    # Hämta data i batch för att inte krascha
    data_batch = yf.Tickers(" ".join(tickers))
    
    for i, ticker in enumerate(tickers):
        with cols[i % 4]:
            try:
                info = data_batch.tickers[ticker].info
                price = info.get('regularMarketPrice') or info.get('currentPrice')
                
                with st.container(border=True):
                    st.metric(ticker, f"{price:,.2f} USD")
                    if st.button(f"Analysera {ticker}", key=f"btn_{ticker}"):
                        if api_key:
                            client = anthropic.Anthropic(api_key=api_key)
                            msg = client.messages.create(
                                model="claude-3-5-sonnet-20240620",
                                max_tokens=200,
                                messages=[{"role": "user", "content": f"Kort analys av {ticker} vid pris {price}."}]
                            )
                            st.write(msg.content[0].text)
                        else:
                            st.warning("Ange API-nyckel")
            except Exception:
                st.write(f"{ticker}: Data ej tillgänglig")
    st.divider()
