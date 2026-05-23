import streamlit as st
import pandas as pd
import numpy as np

# 1. SETUP: Layout och CSS för maximalt utnyttjande
st.set_page_config(page_title="XmarketAi Enterprise", layout="wide")
st.markdown("""<style>.block-container { max-width: 100% !important; }</style>""", unsafe_allow_html=True)

# 2. DATABAS: 30+ Tillgångar uppdelade i kategorier
DB = {
    "AI & Semiconductors": ["NVDA", "AMD", "AVGO", "INTC", "TSM", "ARM"],
    "Space & Future Tech": ["RKLB", "TSLA", "SPCE", "PLTR", "ASTS"],
    "Energy & Data Centers": ["VST", "CEG", "OKLO", "VRT", "NEE", "GEV"],
    "Crypto": ["BTC", "ETH", "SOL", "ADA", "DOT"],
    "AGI & Cloud": ["MSFT", "GOOGL", "AMZN", "META", "ORCL", "SNOW"]
}

st.title("🚀 XmarketAi: Enterprise Command Center")

# 3. NAVIGERING: Flikar för att hantera volymen
tabs = st.tabs(list(DB.keys()))

for i, category in enumerate(DB.keys()):
    with tabs[i]:
        st.subheader(f"Analys: {category}")
        
        # Grid-layout för varje kategori
        cols = st.columns(3)
        for j, ticker in enumerate(DB[category]):
            with cols[j % 3]:
                with st.container(border=True):
                    st.metric(ticker, f"{np.random.randint(10, 80000)} USD")
                    st.line_chart(np.random.normal(100, 10, 20))
                    if st.button(f"Djupanalys {ticker}", key=f"btn_{ticker}_{i}"):
                        st.info(f"AI-Analys för {ticker} laddas...")

# 4. SIDEBAR: Globala verktyg
with st.sidebar:
    st.header("Master Control")
    model = st.selectbox("Välj AI-Analytiker", ["Claude 3.5 Sonnet", "Gemini 1.5 Pro", "Grok"])
    st.write("---")
    st.header("Portfölj-Simulator")
    st.number_input("Total kapital (USD)", value=10000)
    st.button("Optimera Portfölj")
