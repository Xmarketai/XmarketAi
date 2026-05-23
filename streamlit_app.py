import streamlit as st
import yfinance as yf

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Master Dashboard", page_icon="📈", layout="wide")
st.title("📈 XmarketAi: Ultimate Master Dashboard")
st.markdown("### AI, Space, Energy, Semiconductor, Data Center & Crypto")

# --- SIDOMENY FÖR INSTÄLLNINGAR ---
st.sidebar.header("🤖 AI Inställningar")
valda_ai = st.sidebar.selectbox("Välj aktiv AI-analytiker:", ["Gemini", "Claude", "Grok"])
api_key = st.sidebar.text_input(f"{valda_ai} API-nyckel", type="password", help=f"Klistra in din {valda_ai}-nyckel för att aktivera live-analys.")

st.sidebar.markdown("---")

# Tidsväljare för graferna med 15 och 20 år tillagda!
st.sidebar.header("📅 Grafinställningar")
tidsperiod = st.sidebar.selectbox(
    "Välj historik för grafen:",
    options=["1y", "2y", "3y", "5y", "10y", "15y", "20y", "max"],
    format_func=lambda x: (
        "1 år" if x=="1y" else 
        "2 år" if x=="2y" else 
        "3 år" if x=="3y" else 
        "5 år" if x=="5y" else 
        "10 år" if x=="10y" else 
        "15 år" if x=="15y" else 
        "20 år" if x=="20y" else "Max historik"
    )
)

st.sidebar.markdown("---")

# --- REGISTER ÖVER ALLA TILLGÅNGAR ---
tillgangliga_tillgangar = {
    # Krypto
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    # AI & AGI
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
    namn_visning = ticker.replace("-USD", "")
    st.markdown(f"## {namn_visning}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            t = yf.Ticker(ticker)
            historik = t.history(period=tidsperiod)
            
            info = t.info
            pris = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            valuta = "USD" if "-USD" in ticker else info.get("currency", "USD")
            
            if (pris == "N/A" or pris is None) and not historik.empty:
                pris = round(historik['Close'].iloc[-1], 2)
                
            st.metric("Senaste Pris", f"{pris} {valuta}")
            
            if not historik.empty:
                st.write(f"Prisutveckling ({tidsperiod}):")
                st.line_chart(historik['Close'])
                
        except Exception as e:
            st.error(f"Kunde inte hämta data för {ticker}")
            
    with col2:
        st.subheader("📰 Senaste Nyheter & AI")
        
        try:
            nyheter = t.news[:3]
            if nyheter:
                for nyhet in nyheter:
                    st.markdown(f"**[{nyhet['title']}]({nyhet['link']})**")
                    st.caption(f"Källa: {nyhet['publisher']}")
            else:
                st.write("Inga färska nyheter hittades just nu.")
        except:
            st.write("Kunde inte ladda nyhetsflödet.")
            
        st.markdown("---")
        st.write(f"🤖 **{valda_ai}-Analyslaboratorium**")
        
        if st.button(f"Kör {valda_ai}-analys för {namn_visning}", key=f"btn_{ticker}"):
            if not api_key:
                st.warning(f"Klistra in din {valda_ai} API-nyckel i sidomenyn till vänster för att köra live-analys!")
            else:
                st.info(f"Ansluter till {valda_ai} för att analysera marknadsdata, nyheter och historiska trender...")
                
    st.markdown("---")
