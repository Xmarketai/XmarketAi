import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta

# --- 1. KONFIGURATION & SETUP ---
st.set_page_config(page_title="XmarketAi Master Engine", layout="wide", page_icon="📈")
SPARAD_GEMINI_KEY = "AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50"
genai.configure(api_key=SPARAD_GEMINI_KEY)

# --- 2. DATASET: BOLAG & KRIPTO ---
tillgangar_db = {
    "Tesla (TSLA)": {"pris": 426.00, "kat": "Future Tech", "PE": 65, "Trend": "Bullish"},
    "Bitcoin (BTC)": {"pris": 76791.00, "kat": "Crypto", "PE": "N/A", "Trend": "Volatile"},
    "NVIDIA (NVDA)": {"pris": 215.33, "kat": "AI & Semi", "PE": 72, "Trend": "Growth"},
    "Rocket Lab (RKLB)": {"pris": 135.70, "kat": "Space", "PE": "Neg", "Trend": "Speculative"},
    "Vistra Corp (VST)": {"pris": 88.50, "kat": "Energy", "PE": 22, "Trend": "Stable"},
    "Ethereum (ETH)": {"pris": 3500.00, "kat": "Crypto", "PE": "N/A", "Trend": "Neutral"},
    "Solana (SOL)": {"pris": 145.20, "kat": "Crypto", "PE": "N/A", "Trend": "Growth"},
    "Vertiv (VRT)": {"pris": 92.60, "kat": "Data Center", "PE": 45, "Trend": "Strong"}
}

# --- 3. HJÄLPFUNKTIONER FÖR ANALYS ---
def berakna_teknisk_data(pris):
    sma50 = pris * 0.95
    sma200 = pris * 0.85
    rsi = np.random.randint(30, 70)
    return sma50, sma200, rsi

# --- 4. SIDOMENY: KONTROLLPANEL ---
st.sidebar.title("🛠️ Master Engine")
ai_val = st.sidebar.selectbox("Välj AI-Analytiker:", ["Gemini", "Claude", "Grok"])
st.sidebar.info(f"Aktiv motor: {ai_val}")

st.sidebar.header("📊 Filter")
tidsintervall = st.sidebar.selectbox("Analys-vy:", ["Daglig", "Veckovis", "Långsiktig (5år)"])
visa_funda = st.sidebar.checkbox("Visa fundamental analys (PE, Trend)", value=True)

# --- 5. HUVUDDISPLAY: DASHBOARD ---
st.title("⚡ XmarketAi: Executive Decision Engine")
st.markdown("---")

# Dynamiskt nät av tillgångar
cols = st.columns(3)
for i, (namn, data) in enumerate(tillgangar_db.items()):
    with cols[i % 3]:
        st.markdown(f"### {namn}")
        sma50, sma200, rsi = berakna_teknisk_data(data['pris'])
        
        # Metric Cards
        st.metric("Kurs", f"{data['pris']} USD")
        if visa_funda:
            st.caption(f"Kategori: {data['kat']} | PE-Ratio: {data['PE']}")
        
        # AI-Analysknapp
        if st.button(f"Djupanalys: {namn}", key=f"ana_{i}"):
            with st.spinner("AI-motor processar..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Analysera {namn}. Pris: {data['pris']}. RSI: {rsi}. Trend: {data['Trend']}. Är det köp, sälj eller hold för en långsiktig investerare?"
                    res = model.generate_content(prompt)
                    st.success(res.text)
                except:
                    st.error("API-fel: Kontrollera nyckeln.")
        
        # Teknisk vy
        st.line_chart(np.random.normal(data['pris'], 10, 20))
        st.divider()

# --- 6. MASTER ANALYS-TABELL ---
st.header("📋 Master-Matris (Beslutsstöd)")
df = pd.DataFrame(tillgangar_db).T
st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

# --- 7. NYHETS-HUB (HÖGER) ---
st.sidebar.markdown("---")
st.sidebar.subheader("📰 Marknadsinsikter")
st.sidebar.write("• **Tesla:** Fokus på autonomi-day.")
st.sidebar.write("• **NVIDIA:** Ny chip-arkitektur.")
st.sidebar.write("• **Bitcoin:** Institutionellt inflöde ökar.")

# --- 8. PORTFÖLJ-SIMULATOR ---
with st.expander("🧮 Avancerad Portfolio Modeler"):
    st.write("Justera dina vikter för optimal avkastning:")
    weights = {}
    for n in tillgangar_db.keys():
        weights[n] = st.slider(f"Viktning {n} (%)", 0, 100, 10)
    
    total_val = sum([tillgangar_db[n]['pris'] * (w/100) for n, w in weights.items()])
    st.write(f"### Portföljens estimerade värde: {total_val:,.2f} USD")
    st.info("Systemet rekommenderar rebalansering var 30:e dag.")
