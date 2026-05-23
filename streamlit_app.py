import streamlit as st
import yfinance as yf

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Master Dashboard", page_icon="📈", layout="wide")
st.title("📈 XmarketAi: Master Dashboard")
st.markdown("### AI, Space, Energy, Semiconductor, Data Center & Crypto")

# --- SIDOMENY FÖR INSTÄLLNINGAR ---
st.sidebar.header("🤖 AI Inställningar")
GEMINI_KEY = st.sidebar.text_input("Gemini API-nyckel", type="password")
CLAUDE_KEY = st.sidebar.text_input("Claude API-nyckel", type="password")
GROK_KEY = st.sidebar.text_input("Grok API-nyckel", type="password")

st.sidebar.markdown("---")

# --- REGISTER ÖVER ALLA TILLGÅNGAR ---
tillgangliga_tillgangar = {
    # Krypto
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    # AI & AGI (Mjukvara / Moln)
    "Microsoft (MSFT)": "MSFT",
    "Alphabet / Google (GOOGL)": "GOOGL",
    "Meta Platforms (META)": "META",
    "Palantir (PLTR)": "PLTR",
    # Semiconductor / Halvledare
    "NVIDIA (NVDA)": "NVDA",
    "AMD (AMD)": "AMD",
    "Broadcom (AVGO)": "AVGO",
    "TSMC (TSM)": "TSM",
    # Data Center & Infrastruktur
    "Super Micro Computer (SMCI)": "SMCI",
    "Vertiv Holdings (VRT)": "VRT",
    "Arista Networks (ANET)": "ANET",
    # Space / Rymden
    "Rocket Lab (RKLB)": "RKLB",
    "Intuitive Machines (LUNR)": "LUNR",
    # Energy / Energi & Kärnkraft
    "Vistra Corp (VST)": "VST",
    "Bloom Energy (BE)": "BE",
    "Constellation Energy (CEG)": "CEG",
    "Oklo Inc (OKLO)": "OKLO",
    "Tesla (TSLA)": "TSLA"
}

st.sidebar.header("🔍 Välj Tillgångar")
valda_namn = st.sidebar.multiselect(
    "Välj vad du vill övervaka:",
    options=list(tillgangliga_tillgangar.keys()),
    default=["Bitcoin (BTC)", "NVIDIA (NVDA)", "Rocket Lab (RKLB)", "Vistra Corp (VST)", "Tesla (TSLA)"]
)

mina_val = [tillgangliga_tillgangar[namn] for namn in valda_namn]

# --- PROCESSA VARJE TILLGÅNG ---
for ticker in mina_val:
    # Snyggare rubriknamn (ta bort -USD för krypto i visningen)
    namn_visning = ticker.replace("-USD", "")
    st.markdown(f"## {namn_visning}")
    
    try:
        t = yf.Ticker(ticker)
        historik = t.history(period="1y")
        
        info = t.info
        pris = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
        valuta = "USD" if "-USD" in ticker else info.get("currency", "USD")
        
        # Reserv om yfinance saknar direktpris för krypto
        if (pris == "N/A" or pris is None) and not historik.empty:
            pris = round(historik['Close'].iloc[-1], 2)
            
        st.metric("Senaste Pris", f"{pris} {valuta}")
        
        if not historik.empty:
            st.write("Prisutveckling senaste året:")
            st.line_chart(historik['Close'])
            
    except Exception as e:
        st.error(f"Kunde inte hämta data för {ticker}")
    st.markdown("---")
