import streamlit as st
import yfinance as yf
import pandas_ta as ta

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Dashboard", page_icon="🚀", layout="centered")
st.title("🚀 XmarketAi: Dashboard för AI, Space & Energi")

# --- SIDOMENY FÖR INSTÄLLNINGAR ---
st.sidebar.header("🔑 AI Inställningar")
GEMINI_KEY = st.sidebar.text_input("Gemini API-nyckel", type="password")
CLAUDE_KEY = st.sidebar.text_input("Claude API-nyckel", type="password")
GROK_KEY = st.sidebar.text_input("Grok API-nyckel", type="password")

st.sidebar.markdown("---")
st.sidebar.header("📅 Grafinställningar")
tidsperiod = st.sidebar.selectbox(
    "Välj historik för grafen:",
    options=["1y", "2y", "5y", "max"],
    format_func=lambda x: "1 år" if x=="1y" else "2 år" if x=="2y" else "5 år" if x=="5y" else "Max historik",
    index=0
)

# --- FÖRETAGSREGISTER ---
tillgangliga_aktier = {
    "Rocket Lab (RKLB)": "RKLB",
    "Vistra Corp (VST)": "VST",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Apple (AAPL)": "AAPL",
    "Palantir (PLTR)": "PLTR",
    "Amazon (AMZN)": "AMZN",
    "Advanced Micro Devices (AMD)": "AMD"
}

# Nyckelfigurer på X.com
x_profiler = {
    "RKLB": [("Peter Beck (CEO)", "https://x.com/Peter_J_Beck")],
    "TSLA": [("Elon Musk (CEO)", "https://x.com/elonmusk")],
    "MSFT": [("Satya Nadella (CEO)", "https://x.com/satyanadella")]
}

st.sidebar.header("🔍 Välj Bolag")
valda_namn = st.sidebar.multiselect(
    "Välj vilka bolag du vill övervaka på skärmen:",
    options=list(tillgangliga_aktier.keys()),
    default=["Rocket Lab (RKLB)", "Vistra Corp (VST)", "Tesla (TSLA)"]
)

mine_aktier = [tillgangliga_aktier[namn] for namn in valda_namn]

def hemta_aktiedata(ticker_namn, period_val):
    try:
        ticker = yf.Ticker(ticker_namn)
        historik = ticker.history(period=period_val)
        
        if not historik.empty:
            historik.ta.rsi(close='Close', length=14, append=True)
            historik.ta.sma(length=20, append=True) 
            senaste_rsi = historik['RSI_14'].iloc[-1] if 'RSI_14' in historik.columns else "N/A"
        else:
            senaste_rsi = "N/A"
            
        info = ticker.info
        return {
            "namn": info.get("longName", ticker_namn),
            "pris": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "valuta": info.get("currency", "USD"),
            "pe_tal": info.get("trailingPE", "N/A"),
            "rsi": senaste_rsi,
            "historik": historik,
            "nyheter": ticker.news[:3] if ticker.news else []
        }
    except Exception as e:
        return None

# --- PROCESSA VARJE AKTIE ---
for ticker in mine_aktier:
    with st.spinner(f"Hämtar realtidsdata för {ticker}..."):
        data = hemta_aktiedata(ticker, tidsperiod)
        
        if data is None:
            st.error(f"Kunde inte hämta data för {ticker}")
            continue
            
        st.markdown(f"## {data['namn']} ({ticker})")
        
        # Snabba siffror
        col1, col2, col3 = st.columns(3)
        col1.metric("Pris", f"{data['pris']} {data['valuta']}")
        col2.metric("P/E-tal", f"{data['pe_tal']}")
        if isinstance(data['rsi'], float):
            col3.metric("RSI (14)", f"{data['rsi']:.2f}")
        else:
            col3.metric("RSI (14)", f"{data['rsi']}")
        
        # Teknisk Graf
        if not data['historik'].empty:
            st.write(f"**Teknisk Analys (Pris vs 20 SMA över {tidsperiod}):**")
            kolumner_att_visa = ['Close']
            if 'SMA_20' in data['historik'].columns:
                kolumner_att_visa.append('SMA_20')
            graf_data = data['historik'][kolumner_att_visa]
            st.line_chart(graf_data)
            
        # X.com Länkar
        if ticker in x_profiler:
            st.write("🐦 **Viktiga X.com Profiler & Nyckelfigurer:**")
            cols = st.columns(len(x_profiler[ticker]))
            for idx, (namn, lank) in enumerate(x_profiler[ticker]):
                cols[idx].markdown(f"[🔗 Gå till {namn}]({lank})")
        
        # AI-Analys flikar
        st.write("🤖 **AI-Agentens Utlåtanden:**")
        tab1, tab2, tab3 = st.tabs(["Gemini Syn", "Claude Syn", "Grok Syn"])
        
        with tab2:
            st.warning("Ange Gemini-nyckel i menyn för djupanalys.")
        with tab2:
            st.warning("Ange Claude-nyckel för långsiktig AGI-trend.")
        with tab3:
            st.warning("Ange Grok-nyckel för X-plattformsanalys.")
                
        # Nyhetsflöde
        with st.expander("📰 Senaste Nyheter & Pressmeddelanden"):
            if data['nyheter']:
                for n in data['nyheter']:
                    rubrik = n.get('title', 'Nyhet')
                    lank = n.get('link', '#')
                    kalla = n.get('publisher', 'Okänd källa')
                    st.markdown(f"**[{rubrik}]({lank})**")
                    st.caption(f"Källa: {kalla}")
            else:
                st.write("Inga färska nyheter hittades just nu.")
        st.markdown("---")
