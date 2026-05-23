import streamlit as st
import yfinance as yf

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Dashboard", page_icon="🚀")
st.title("🚀 XmarketAi: Dashboard")

st.sidebar.header("🔍 Välj Bolag")
valda_namn = st.sidebar.multiselect(
    "Välj bolag:",
    options=["Rocket Lab (RKLB)", "Vistra Corp (VST)", "Tesla (TSLA)", "NVIDIA (NVDA)"],
    default=["Rocket Lab (RKLB)", "Tesla (TSLA)"]
)

tillgangliga_aktier = {
    "Rocket Lab (RKLB)": "RKLB",
    "Vistra Corp (VST)": "VST",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA"
}

mine_aktier = [tillgangliga_aktier[namn] for namn in valda_namn]

# --- PROCESSA VARJE AKTIE ---
for ticker in mine_aktier:
    st.markdown(f"## Bolag: {ticker}")
    try:
        t = yf.Ticker(ticker)
        historik = t.history(period="1y")
        
        info = t.info
        pris = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        valuta = info.get("currency", "USD")
        
        st.metric("Senaste Pris", f"{pris} {valuta}")
        
        if not historik.empty:
            st.write("Prisutveckling senaste året:")
            st.line_chart(historik['Close'])
    except Exception as e:
        st.error(f"Kunde inte hämta data för {ticker}")
    st.markdown("---")
