import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta

# --- 1. PREMIUM ARKITEKTUR ---
st.set_page_config(page_title="XmarketAi Master Engine", page_icon="⚡", layout="wide")

# CSS för mobilanpassning och "Pro-Look"
st.markdown("""
    <style>
    .main-title { font-size: 2.8rem; font-weight: 900; color: #1E1E1E; text-align: center; }
    .card { background-color: #fcfcfc; border: 1px solid #e0e0e0; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MASTER DATABAS (Single Source of Truth) ---
ASSET_DB = {
    "Bitcoin (BTC)": {"pris": 76791.00, "kat": "Crypto", "kod": "BTC"},
    "Ethereum (ETH)": {"pris": 2120.53, "kat": "Crypto", "kod": "ETH"},
    "Solana (SOL)": {"pris": 145.00, "kat": "Crypto", "kod": "SOL"},
    "NVIDIA (NVDA)": {"pris": 215.33, "kat": "AI & Semi", "kod": "NVDA"},
    "AMD (AMD)": {"pris": 155.20, "kat": "AI & Semi", "kod": "AMD"},
    "Tesla (TSLA)": {"pris": 426.00, "kat": "Future Tech", "kod": "TSLA"},
    "Rocket Lab (RKLB)": {"pris": 135.70, "kat": "Space", "kod": "RKLB"},
    "Vistra Corp (VST)": {"pris": 112.10, "kat": "Energy", "kod": "VST"},
    "Constellation (CEG)": {"pris": 225.00, "kat": "Energy", "kod": "CEG"},
    "Oklo (OKLO)": {"pris": 15.40, "kat": "Energy", "kod": "OKLO"},
    "Vertiv (VRT)": {"pris": 92.60, "kat": "Data Center", "kod": "VRT"}
}

# --- 3. LOGIK-MOTOR (Klassbaserad för stabilitet) ---
class MarketEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def get_analysis(self, namn, pris):
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(f"Analysera {namn} till {pris} USD. Investeringstyp: långsiktig. Ge köpråd.").text

    def generate_chart_data(self, pris):
        # Skapar en stabil prisbana
        dates = pd.date_range(start=datetime.now()-timedelta(days=365), periods=100)
        vals = np.random.normal(pris, pris*0.05, 100)
        return pd.DataFrame({'Pris': vals}, index=dates)

# Initiera motor
engine = MarketEngine("AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50")

# --- 4. DASHBOARD LAYOUT ---
st.markdown('<div class="main-title">⚡ XmarketAi: Master Engine</div>', unsafe_allow_html=True)

# Sidomeny för filter
with st.sidebar:
    st.header("⚙️ Kontrollpanel")
    valda = st.multiselect("Bevakningslista:", list(ASSET_DB.keys()), default=list(ASSET_DB.keys())[:3])
    tidsvy = st.selectbox("Tidsvy:", ["1 Månad", "1 År", "Max"])
    st.info("Systemstatus: **Online**")

# Loop för tillgångar
for namn in valda:
    info = ASSET_DB[namn]
    with st.container():
        st.markdown(f"### 📈 {namn}")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.metric("Pris", f"{info['pris']:,} USD")
            if st.button(f"Analysera {info['kod']}", key=f"btn_{namn}"):
                with st.spinner("AI-motor arbetar..."):
                    st.success(engine.get_analysis(namn, info['pris']))
        
        with col2:
            st.line_chart(engine.generate_chart_data(info['pris']))
            
        with col3:
            st.write(f"**Kategori:** {info['kat']}")
            vol = st.slider(f"Portföljvikt {info['kod']}", 0, 100, 10)
            st.write(f"Värde: {info['pris'] * (vol/100):.2f} USD")
        st.markdown("---")

# --- 5. MASTER MATRIS (Beslutsstöd) ---
st.header("📋 Master-Matris: Snabbanalys")
df = pd.DataFrame(ASSET_DB).T
st.dataframe(df.style.background_gradient(subset=['pris']), use_container_width=True)

# --- 6. UTÖKAD FUNKTIONALITET (Nyheter & Simulator) ---
col_n1, col_n2 = st.columns(2)
with col_n1:
    st.subheader("📰 Marknadshub")
    st.write("• **Tesla:** Fokus på energilagring och FSD.")
    st.write("• **NVIDIA:** Fortsatt dominans inom AI-infrastruktur.")
with col_n2:
    st.subheader("🧮 Simulator")
    st.write("Simulera din portföljs framtida utveckling baserat på AI-estimat.")
