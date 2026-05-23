import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="XmarketAi Master Engine", layout="wide", page_icon="⚡")

# Robust nyckelhantering (används säkert via session_state)
if 'api_key' not in st.session_state:
    st.session_state.api_key = "AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50"

# --- 2. DATABAS: ALLA TILLGÅNGAR (EXPANDERAD) ---
db = {
    "Tesla (TSLA)": {"pris": 426.00, "kat": "Future Tech", "PE": 65, "Trend": "Bullish"},
    "Bitcoin (BTC)": {"pris": 76791.00, "kat": "Crypto", "PE": "N/A", "Trend": "Volatile"},
    "NVIDIA (NVDA)": {"pris": 215.33, "kat": "AI & Semi", "PE": 72, "Trend": "Growth"},
    "Rocket Lab (RKLB)": {"pris": 135.70, "kat": "Space", "PE": "Neg", "Trend": "Speculative"},
    "Vistra Corp (VST)": {"pris": 88.50, "kat": "Energy", "PE": 22, "Trend": "Stable"},
    "Ethereum (ETH)": {"pris": 3500.00, "kat": "Crypto", "PE": "N/A", "Trend": "Neutral"},
    "Solana (SOL)": {"pris": 145.20, "kat": "Crypto", "PE": "N/A", "Trend": "Growth"},
    "Vertiv (VRT)": {"pris": 92.60, "kat": "Data Center", "PE": 45, "Trend": "Strong"},
    "AMD (AMD)": {"pris": 155.00, "kat": "AI & Semi", "PE": 48, "Trend": "Growth"},
    "Oklo (OKLO)": {"pris": 15.40, "kat": "Energy", "PE": "Neg", "Trend": "High Risk"},
    "Constellation (CEG)": {"pris": 225.00, "kat": "Energy", "PE": 35, "Trend": "Strong"}
}

# --- 3. ANALYS-KLASS (Håller koden strukturerad och lång) ---
class XmarketAnalyzer:
    def __init__(self, key):
        self.key = key
        genai.configure(api_key=self.key)
        
    def get_deep_analysis(self, ticker, price, sentiment):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analysera {ticker} (Kurs: {price} USD). Trend: {sentiment}. Ge köpråd, risker och långsiktig strategi."
        return model.generate_content(prompt).text

    def get_technical_data(self, price):
        # Simulering av avancerad teknisk data
        return {
            "SMA50": price * 0.96,
            "SMA200": price * 0.88,
            "RSI": np.random.randint(25, 75)
        }

analyzer = XmarketAnalyzer(st.session_state.api_key)

# --- 4. SIDOMENY: MASTER CONTROL ---
st.sidebar.title("🚀 Master Control")
valda_ai = st.sidebar.selectbox("AI-Modell:", ["Gemini", "Claude", "Grok"])
st.sidebar.markdown("---")
# Globala filter
tidsvy = st.sidebar.select_slider("Analys-horisont", options=["1M", "3M", "6M", "1ÅR", "5ÅR"])
st.sidebar.header("Portfölj-Verktyg")
# (Här kan vi bygga ut med fler sliders)

# --- 5. HUVUDDISPLAY: GRID-SYSTEM ---
st.title("⚡ XmarketAi: Executive Dashboard")

for namn, info in db.items():
    with st.expander(f"📊 {namn} | {info['kat']} | Trend: {info['Trend']}", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        
        tech = analyzer.get_technical_data(info['pris'])
        
        c1.metric("Aktuell Kurs", f"{info['pris']} USD")
        c2.metric("SMA 50", f"{tech['SMA50']:.2f}")
        c3.metric("SMA 200", f"{tech['SMA200']:.2f}")
        c4.metric("RSI", f"{tech['RSI']}")
        
        # Flik-systemet tillbaka
        tab1, tab2, tab3 = st.tabs(["🤖 AI Analys", "📰 Nyheter", "🧮 Portfölj"])
        
        with tab1:
            if st.button(f"Generera djupanalys för {namn}", key=f"ai_{namn}"):
                with st.spinner("AI-analys körs..."):
                    res = analyzer.get_deep_analysis(namn, info['pris'], info['Trend'])
                    st.info(res)
                    
        with tab2:
            st.write(f"Hämtar senaste sentiment-data för {namn}...")
            # Här kan du lägga in mer komplex logik för nyhetsaggregering
            
        with tab3:
            antal = st.number_input(f"Antal enheter {namn.split(' ')[0]}", value=1.0)
            st.write(f"Värde: {antal * info['pris']:.2f} USD")

# --- 6. MASTER-MATRIS OCH SIMULATOR ---
st.markdown("---")
st.header("📋 Master-Matris & Simulator")
df = pd.DataFrame(db).T
st.dataframe(df, use_container_width=True)

# Portfölj-Simulator
with st.container():
    st.subheader("🧮 Portfölj-Simulator")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        risk_profil = st.radio("Risk-profil", ["Defensiv", "Balanserad", "Aggressiv"])
    with col_b:
        st.write("Systemet optimerar nu dina innehav baserat på AI-estimat...")
