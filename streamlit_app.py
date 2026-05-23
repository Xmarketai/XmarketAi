import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta

st.set_page_config(page_title="XmarketAi Pro", layout="wide")

# API-NYCKEL (Låst och korrekt)
SPARAD_GEMINI_KEY = "AIzaSyDy6tOqejFsyLUR6SjgfWoXfyNPGNYeM50"
genai.configure(api_key=SPARAD_GEMINI_KEY)

st.title("⚡ XmarketAi Dashboard")

# BOLAGSREGISTER (Tesla uppdaterat till 426 USD)
tillgangar = {
    "Tesla (TSLA)": {"aktuellt_pris": 426.00, "kat": "Future Tech", "kod": "TSLA"},
    "Bitcoin (BTC)": {"aktuellt_pris": 76791.00, "kat": "Crypto", "kod": "BTC"},
    "NVIDIA (NVDA)": {"aktuellt_pris": 215.33, "kat": "AI & Semi", "kod": "NVDA"}
}

valda_namn = st.multiselect("Välj tillgångar:", list(tillgangar.keys()), default=["Tesla (TSLA)"])

for namn in valda_namn:
    info = tillgangar[namn]
    st.subheader(f"📈 {namn}")
    st.metric("Pris", f"{info['aktuellt_pris']} USD")
    
    if st.button(f"Kör AI-analys för {info['kod']}", key=f"btn_{info['kod']}"):
        with st.spinner("Analyserar..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Analysera {namn} till priset {info['aktuellt_pris']} USD. Kort och koncist.")
                st.info(response.text)
            except Exception as e:
                st.error(f"Kopplingsfel: {e}")
