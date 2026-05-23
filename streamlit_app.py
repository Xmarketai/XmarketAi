import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

# --- 1. PREMIUM MOBILOPTIMERAD DESIGN ---
st.set_page_config(page_title="XmarketAi Pro Dashboard", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #FF4B4B; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.0rem; text-align: center; color: #666; margin-bottom: 20px; }
    @media (max-width: 640px) {
        .main-title { font-size: 1.6rem; }
        .stButton button { width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ XmarketAi: Ultimate Master Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI, Space, Energy, Semiconductors, Data Centers & Crypto</div>', unsafe_allow_html=True)

# --- 2. DIN GEMINI-NYCKEL (LÅST OCH KLAR) ---
# Här ligger din fungerande nyckel nu helt korrekt på rad 26
SPARAD_GEMINI_KEY = "AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50"

# --- 3. SYSTEMINSTÄLLNINGAR I SIDOMENYN ---
st.sidebar.header("🤖 AI-Inställningar")
valda_ai = st.sidebar.selectbox("Aktiv AI-Analytiker:", ["Gemini", "Claude", "Grok"])

if valda_ai == "Gemini" and SPARAD_GEMINI_KEY != "DIN_RIKTIGA_GEMINI_NYCKEL_HÄR":
    api_key = SPARAD_GEMINI_KEY
    st.sidebar.success("✅ Gemini-nyckel aktiv!")
else:
    api_key = st.sidebar.text_input(f"{valda_ai} API-nyckel", type="password")

st.sidebar.markdown("---")
st.sidebar.header("📅 Tidsintervall")
tidsperiod = st.sidebar.selectbox(
    "Välj historik för grafer:",
    options=["1 Månad", "3 Månader", "6 Månader", "1 År", "3 År", "5 År"],
    index=3
)

st.sidebar.header("📊 Tekniska Indikatorer")
visa_sma = st.sidebar.checkbox("Glidande Medelvärde (SMA 20)", value=True)
visa_rsi = st.sidebar.checkbox("Visa RSI (Momentum-bevakning)", value=True)

# --- 4. DET KOMPLETTA BOLAGSREGISTRET ---
tillgangar = {
    "Bitcoin (BTC)": {"aktuellt_pris": 76791.00, "kat": "Crypto", "kod": "BTC"},
    "Ethereum (ETH)": {"aktuellt_pris": 2125.90, "kat": "Crypto", "kod": "ETH"},
    "Solana (SOL)": {"aktuellt_pris": 145.00, "kat": "Crypto", "kod": "SOL"},
    "NVIDIA (NVDA)": {"aktuellt_pris": 215.30, "kat": "AI & Semi", "kod": "NVDA"},
    "AMD (AMD)": {"aktuellt_pris": 155.20, "kat": "AI & Semi", "kod": "AMD"},
    "Tesla (TSLA)": {"aktuellt_pris": 175.80, "kat": "Future Tech", "kod": "TSLA"},
    "Rocket Lab (RKLB)": {"aktuellt_pris": 135.70, "kat": "Space", "kod": "RKLB"},
    "Vistra Corp (VST)": {"aktuellt_pris": 112.10, "kat": "Energy", "kod": "VST"},
    "Constellation Energy (CEG)": {"aktuellt_pris": 225.00, "kat": "Energy", "kod": "CEG"},
    "Oklo Inc (OKLO)": {"aktuellt_pris": 15.40, "kat": "Energy", "kod": "OKLO"},
    "Vertiv Holdings (VRT)": {"aktuellt_pris": 92.60, "kat": "Data Center", "kod": "VRT"}
}

st.sidebar.header("🔍 Hantera Bevakningslista")
valda_namn = st.sidebar.multiselect(
    "Välj tillgångar att visa på skärmen:",
    options=list(tillgangar.keys()),
    default=["Bitcoin (BTC)", "NVIDIA (NVDA)", "Rocket Lab (RKLB)", "Tesla (TSLA)"]
)

# --- 5. STABIL TRADING-MOTOR (Låsta priser utifrån valda_namn) ---
def generera_stabil_kurshistorik(namn, slutpris, period_val):
    dagar_mappning = {"1 Månad": 30, "3 Månader": 90, "6 Månader": 180, "1 År": 365, "3 År": 1095, "5 År": 1825}
    antal_dagar = dagar_mappning[period_val]
    
    np.random.seed(sum(ord(c) for c in namn))
    start_date = datetime.now() - timedelta(days=antal_dagar)
    dates = pd.date_range(start=start_date, periods=antal_dagar, freq='D')
    
    forandringar = np.random.normal(0.0003, 0.018, antal_dagar)
    pris_bana = np.zeros(antal_dagar)
    pris_bana[-1] = slutpris
    
    for i in range(antal_dagar - 2, -1, -1):
        pris_bana[i] = pris_bana[i+1] / (1 + forandringar[i])
        
    df = pd.DataFrame(index=dates)
    df['Pris'] = np.round(pris_bana, 2)
    
    df['SMA_20'] = df['Pris'].rolling(window=20).mean()
    delta = df['Pris'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)
    
    return df

# --- 6. BYGG MOBILVÄNLIGA KORT OCH FLIKAR ---
if not valda_namn:
    st.info("💡 Välj tillgångar i sidomenyn till vänster för att starta!")
else:
    for namn in valda_namn:
        info = tillgangar[namn]
        df_data = generera_stabil_kurshistorik(namn, info["aktuellt_pris"], tidsperiod)
        
        senaste_pris = df_data['Pris'].iloc[-1]
        foregaende_pris = df_data['Pris'].iloc[-2]
        procent_ändring = ((senaste_pris - foregaende_pris) / foregaende_pris) * 100
        nuvarande_rsi = round(df_data['RSI'].iloc[-1], 2)
        
        st.markdown(f"### 📈 {namn} — <span style='color:gray; font-size:0.9rem;'>{info['kat']}</span>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
        with m1:
            st.metric("Senaste Pris", f"{senaste_pris:,} USD".replace(",", " "), f"{procent_ändring:.2f}%")
        with m2:
            st.metric("Högsta (Perioden)", f"{df_data['Pris'].max():,} USD".replace(",", " "))
        with m3:
            st.metric("Lägsta (Perioden)", f"{df_data['Pris'].min():,} USD".replace(",", " "))
        with m4:
            if visa_rsi:
                status_rsi = "Överköpt 🔴" if nuvarande_rsi > 70 else "Översåld 🟢" if nuvarande_rsi < 30 else "Neutral 🟡"
                st.metric("RSI (14)", f"{nuvarande_rsi}", status_rsi)

        graf_df = pd.DataFrame(index=df_data.index)
        graf_df['Marknadspris'] = df_data['Pris']
        if visa_sma:
            graf_df['SMA 20'] = df_data['SMA_20']
            
        st.line_chart(graf_df)
        
        flik_ai, flik_nyheter, flik_verktyg = st.tabs(["🤖 AI Analys", "📰 Marknadsnyheter", "🧮 Portfölj-Simulator"])
        
        with flik_ai:
            if st.button(f"Kör intelligent {valda_ai}-analys för {info['kod']}", key=f"ai_{info['kod']}"):
                with st.spinner(f"Ansluter till {valda_ai} AI-motor..."):
                    # NY MODERN STRUKTUR FÖR GEMINI API-ANROP
                    headers = {'Content-Type': 'application/json'}
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": f"Gör en kort marknadsanalys på svenska av {namn} ({info['kod']}) baserat på att priset står i {senaste_pris} USD och RSI är {nuvarande_rsi}. Ge en köp/sälj/avvakta-tendens."
                            }]
                        }]
                    }
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        res = requests.post(url, headers=headers, json=payload)
                        output_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.info(output_text)
                    except:
                        st.error("Det gick inte att hämta analysen. Kontrollera att din API-nyckel inte har några begränsningar i Google Cloud.")
                        
        with flik_nyheter:
            st.markdown(f"**🔥 Senaste rubrikerna för {info['kod']}:**")
            st.markdown(f"* **[VOLATILITY]** Stora institutionella blockorder har registrerats i {namn} under morgonhandeln.")
            st.markdown(f"* **[SECTOR NEWS]** Ökad efterfrågan inom {info['kat']} skapar starkt fundamentalt stöd.")
            
        with flik_verktyg:
            antal_aktier = st.number_input(f"Innehav i {info['kod']}:", min_value=0.0, value=10.0, key=f"calc_{info['kod']}")
            st.success(f"Ditt simulerade innehav är värt: **{antal_aktier * senaste_pris:,.2f} USD**".replace(",", " "))

        st.markdown("---")
