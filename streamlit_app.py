import streamlit as st
import yfinance as yf
import requests
import json

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Master Dashboard", page_icon="📈", layout="wide")
st.title("📈 XmarketAi: Ultimate Master Dashboard")
st.markdown("### AI, Space, Energy, Semiconductor, Data Center & Crypto")

# --- SIDOMENY FÖR INSTÄLLNINGAR ---
st.sidebar.header("🤖 AI Inställningar")
valda_ai = st.sidebar.selectbox("Välj aktiv AI-analytiker:", ["Gemini", "Claude", "Grok"])
api_key = st.sidebar.text_input(f"{valda_ai} API-nyckel", type="password", help=f"Klistra in din {valda_ai}-nyckel.")

st.sidebar.markdown("---")

st.sidebar.header("📅 Grafinställningar")
tidsperiod = st.sidebar.selectbox(
    "Välj historik för grafen:",
    options=["1y", "2y", "3y", "5y", "10y", "15y", "20y", "max"],
    format_func=lambda x: f"{x.replace('max', 'Max historik').replace('y', ' år')}"
)

st.sidebar.markdown("---")

# --- REGISTER ÖVER ALLA TILLGÅNGAR ---
tillgangliga_tillgangar = {
    "Bitcoin (BTC)": "BTC-USD", "Ethereum (ETH)": "ETH-USD", "Solana (SOL)": "SOL-USD",
    "Microsoft (MSFT)": "MSFT", "Alphabet / Google (GOOGL)": "GOOGL", "Meta Platforms (META)": "META", "Palantir (PLTR)": "PLTR",
    "NVIDIA (NVDA)": "NVDA", "AMD (AMD)": "AMD", "Broadcom (AVGO)": "AVGO", "TSMC (TSM)": "TSM",
    "Super Micro Computer (SMCI)": "SMCI", "Vertiv Holdings (VRT)": "VRT", "Arista Networks (ANET)": "ANET",
    "Rocket Lab (RKLB)": "RKLB", "Intuitive Machines (LUNR)": "LUNR",
    "Vistra Corp (VST)": "VST", "Bloom Energy (BE)": "BE", "Constellation Energy (CEG)": "CEG", "Oklo Inc (OKLO)": "OKLO", "Tesla (TSLA)": "TSLA"
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
    current_ticker = yf.Ticker(ticker)
    
    with col1:
        try:
            historik = current_ticker.history(period=tidsperiod)
            info = current_ticker.info
            pris = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            valuta = "USD" if "-USD" in ticker else info.get("currency", "USD")
            
            if (pris == "N/A" or pris is None) and not historik.empty:
                pris = round(historik['Close'].iloc[-1], 2)
                
            st.metric("Senaste Pris", f"{pris} {valuta}")
            if not historik.empty:
                st.line_chart(historik['Close'])
        except:
            st.error(f"Kunde inte hämta marknadsdata.")
            
    with col2:
        st.subheader("📰 Senaste Nyheter & AI Insights")
        
        try:
            nyheter = current_ticker.news[:3]
            if nyheter:
                for nyhet in nyheter:
                    st.markdown(f"**[{nyhet['title']}]({nyhet['link']})**")
                    st.caption(f"Källa: {nyhet['publisher']}")
            else:
                st.write("Inga färska nyheter hittades på Yahoo just nu.")
        except:
            st.write("Nyhetsflöde tillfälligt ej tillgängligt.")
            
        st.markdown("---")
        st.write(f"🤖 **{valda_ai}-Analyslaboratorium**")
        
        if st.button(f"Kör {valda_ai}-analys för {namn_visning}", key=f"btn_{ticker}"):
            if not api_key:
                st.warning(f"Klistra in din {valda_ai} API-nyckel till vänster!")
            else:
                with st.spinner(f"Ansluter till {valda_ai} för att analysera {namn_visning}..."):
                    prompt = f"Gör en kort, skarp och professionell framtidsanalys av {namn_visning} ({ticker}) på svenska baserat på dess marknadsposition. Vad är de viktigaste trenderna just nu?"
                    
                    try:
                        if valda_ai == "Gemini":
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                            headers = {'Content-Type': 'application/json'}
                            payload = {"contents": [{"parts": [{"text": prompt}]}]}
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                            
                        elif valda_ai == "Claude":
                            url = "https://api.anthropic.com/v1/messages"
                            headers = {
                                "x-api-key": api_key,
                                "anthropic-version": "2023-06-01",
                                "content-type": "application/json"
                            }
                            payload = {
                                "model": "claude-3-5-sonnet-20241022",
                                "max_tokens": 1000,
                                "messages": [{"role": "user", "content": prompt}]
                            }
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['content'][0]['text'])
                            
                        elif valda_ai == "Grok":
                            url = "https://api.x.ai/v1/chat/completions"
                            headers = {
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            }
                            payload = {
                                "model": "grok-beta",
                                "messages": [{"role": "user", "content": prompt}]
                            }
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['choices'][0]['message']['content'])
                            
                    except Exception as e:
                        st.error("Kopplingen misslyckades. Kontrollera att din API-nyckel är helt korrekt kopierad utan mellanslag!")
                        
    st.markdown("---")
