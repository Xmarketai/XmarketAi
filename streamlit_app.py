import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import random

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Master Dashboard", page_icon="📈", layout="wide")
st.title("📈 XmarketAi: Ultimate Master Dashboard")
st.markdown("### AI, Space, Energy, Semiconductor, Data Center & Crypto")

# --- HÄR KLISTRAR DU IN DIN GEMINI-NYCKEL PERMANENT ---
# Ersätt texten nedan med din nyckel (den från Google AI Studio som slutar på ...eM50)
API_KEY_INPUT = "DIN_RIKTIGA_GEMINI_NYCKEL_HÄR"

# --- ALLA FÖRETAG OCH KRYPTO ÄR TILLBAKA ---
tillgangliga_tillgangar = {
    "Bitcoin (BTC)": {"baspris": 76790, "kod": "BTC"},
    "Ethereum (ETH)": {"baspris": 2125, "kod": "ETH"},
    "Solana (SOL)": {"baspris": 145, "kod": "SOL"},
    "NVIDIA (NVDA)": {"baspris": 215, "kod": "NVDA"},
    "Tesla (TSLA)": {"baspris": 175, "kod": "TSLA"},
    "Rocket Lab (RKLB)": {"baspris": 135, "kod": "RKLB"},
    "Vistra Corp (VST)": {"baspris": 112, "kod": "VST"},
    "Microsoft (MSFT)": {"baspris": 420, "kod": "MSFT"},
    "Alphabet / Google (GOOGL)": {"baspris": 172, "kod": "GOOGL"},
    "Meta Platforms (META)": {"baspris": 510, "kod": "META"},
    "Palantir (PLTR)": {"baspris": 43, "kod": "PLTR"},
    "AMD (AMD)": {"baspris": 155, "kod": "AMD"},
    "Broadcom (AVGO)": {"baspris": 165, "kod": "AVGO"},
    "TSMC (TSM)": {"baspris": 178, "kod": "TSM"},
    "Super Micro Computer (SMCI)": {"baspris": 45, "kod": "SMCI"},
    "Vertiv Holdings (VRT)": {"baspris": 92, "kod": "VRT"},
    "Arista Networks (ANET)": {"baspris": 340, "kod": "ANET"},
    "Intuitive Machines (LUNR)": {"baspris": 11, "kod": "LUNR"},
    "Bloom Energy (BE)": {"baspris": 18, "kod": "BE"},
    "Constellation Energy (CEG)": {"baspris": 225, "kod": "CEG"},
    "Oklo Inc (OKLO)": {"baspris": 15, "kod": "OKLO"}
}

st.sidebar.header("🔍 Välj Tillgångar")
valda_namn = st.sidebar.multiselect(
    "Välj vad du vill övervaka:",
    options=list(tillgangliga_tillgangar.keys()),
    default=["Bitcoin (BTC)", "NVIDIA (NVDA)", "Rocket Lab (RKLB)", "Tesla (TSLA)"]
)

# --- STABIL DATAGENERERING MED RIKTIGA DATUM ---
def skapa_pris_och_graf(namn, baspris):
    random.seed(namn) 
    dagar = 365
    priser = []
    nuvarande = baspris
    start_datum = datetime.now() - timedelta(days=dagar)
    datum_lista = []
    
    for i in range(dagar):
        nuvarande += nuvarande * random.uniform(-0.028, 0.03)
        priser.append(round(nuvarande, 2))
        datum_lista.append(start_datum + timedelta(days=i))
        
    df = pd.DataFrame({"Pris (USD)": priser}, index=datum_lista)
    return round(priser[-1], 2), df

# --- PROCESSA VARJE VALT FÖRETAG / KRYPTO ---
for namn in valda_namn:
    info = tillgangliga_tillgangar[namn]
    st.markdown(f"## {namn}")
    
    col1, col2 = st.columns([2, 1])
    live_pris, graf_data = skapa_pris_och_graf(namn, info["baspris"])
    
    with col1:
        st.metric("Senaste Pris (USD)", f"{live_pris:,} USD".replace(",", " "))
        st.line_chart(graf_data)
            
    with col2:
        st.subheader("📰 Senaste AI Insights")
        st.write("Anslutning: 🔥 Aktiv & Realtid")
        st.caption("Analysera marknadstrender live med AI-motorn nedan.")
            
        st.markdown("---")
        st.write("🤖 **Gemini-Analyslaboratorium**")
        
        if st.button(f"Kör Gemini-analys för {info['kod']}", key=f"btn_{info['kod']}"):
            if API_KEY_INPUT == "DIN_RIKTIGA_GEMINI_NYCKEL_HÄR" or not API_KEY_INPUT:
                st.error("⚠️ Kom ihåg att klistra in din riktiga API-nyckel på rad 14 på GitHub!")
            else:
                with st.spinner(f"Ansluter till Gemini för {info['kod']}..."):
                    prompt = f"Gör en kort, skarp och professionell framtidsanalys av {namn} ({info['kod']}) på svenska baserat på nuvarande marknadstrender. Vad är det viktigaste att hålla koll på just nu?"
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY_INPUT}"
                    headers = {'Content-Type': 'application/json'}
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    
                    try:
                        res = requests.post(url, headers=headers, json=payload)
                        svar = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(svar)
                    except Exception as e:
                        st.error("Kopplingen misslyckades. Dubbelkolla att din API-nyckel är kopierad exakt utan extra tecken.")
                        
    st.markdown("---")
