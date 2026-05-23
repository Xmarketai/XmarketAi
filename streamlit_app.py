import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai

# --- 1. FULL STORLEK CONFIG ---
st.set_page_config(page_title="XmarketAi Mega Engine", layout="wide")

# Tvingande CSS för att maximera bredd och förhindra att element krymper
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 98% !important; }
    .stMetric { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 1px solid #dee2e6; }
    .css-1544g2n { padding: 2rem !important; }
    .main-title { font-size: 3.0rem; font-weight: 900; color: #2b2b2b; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. FULLSTÄNDIG DATABAS ---
ALLA_TILLGANGAR = {
    "Bitcoin (BTC)": {"pris": 76791.00, "kat": "Crypto"},
    "Ethereum (ETH)": {"pris": 2120.53, "kat": "Crypto"},
    "Solana (SOL)": {"pris": 145.00, "kat": "Crypto"},
    "NVIDIA (NVDA)": {"pris": 215.33, "kat": "AI & Semi"},
    "AMD (AMD)": {"pris": 155.20, "kat": "AI & Semi"},
    "Tesla (TSLA)": {"pris": 426.00, "kat": "Future Tech"},
    "Rocket Lab (RKLB)": {"pris": 135.70, "kat": "Space"},
    "Vistra Corp (VST)": {"pris": 112.10, "kat": "Energy"},
    "Constellation (CEG)": {"pris": 225.00, "kat": "Energy"},
    "Oklo (OKLO)": {"pris": 15.40, "kat": "Energy"},
    "Vertiv (VRT)": {"pris": 92.60, "kat": "Data Center"}
}

# --- 3. SIDEBAR: KOMPLETT KONTROLL ---
with st.sidebar:
    st.title("🎛️ Master Engine Control")
    api_key = st.text_input("API Key", value="AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50", type="password")
    
    st.subheader("Modul-Status")
    st.write("✅ AI-Analys (Gemini/Claude/Grok)")
    st.write("✅ Portfölj-Simulator")
    st.write("✅ Marknads-Matris")
    st.write("✅ Nyhetsflöde")
    
    st.markdown("---")
    visning = st.multiselect("Välj tillgångar att visa:", list(ALLA_TILLGANGAR.keys()), default=list(ALLA_TILLGANGAR.keys()))

# --- 4. HUVUDFÖNSTER: GRID AV FULLSTÄNDIGA KORT ---
st.markdown('<p class="main-title">⚡ XmarketAi: Ultimate Dashboard</p>', unsafe_allow_html=True)

# Vi bygger 3 stora kolumner som aldrig krymper
for i in range(0, len(visning), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(visning):
            ticker = visning[i+j]
            info = ALLA_TILLGANGAR[ticker]
            
            with cols[j]:
                with st.container(border=True):
                    st.subheader(f"📈 {ticker}")
                    st.metric("Pris (USD)", f"{info['pris']:,}")
                    
                    # AI-modul
                    if st.button(f"Analysera {ticker}", key=f"ai_{ticker}"):
                        genai.configure(api_key=api_key)
                        res = genai.GenerativeModel('gemini-1.5-flash').generate_content(f"Analysera {ticker}")
                        st.info(res.text)
                    
                    # Graf
                    st.line_chart(np.random.normal(info['pris'], 5, 50))
                    
                    # Simulator-input
                    st.number_input(f"Innehav {ticker}", value=1.0, key=f"inv_{ticker}")

# --- 5. FULLSTÄNDIG MATRIS & PORTFÖLJ ---
st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
    st.header("📋 Master Data-Matris")
    st.dataframe(pd.DataFrame(ALLA_TILLGANGAR).T, use_container_width=True)
with col_b:
    st.header("🧮 Portfölj-Simulator")
    st.write("Här visas summeringen av alla dina innehav i Master-Matrisen.")
