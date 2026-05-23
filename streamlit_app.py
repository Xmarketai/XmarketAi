import streamlit as st
import requests
import pandas as pd

# --- APP-KONFIGURATION ---
st.set_page_config(page_title="XmarketAi Master Dashboard", page_icon="📈", layout="wide")
st.title("📈 XmarketAi: Ultimate Master Dashboard")
st.markdown("### AI, Space, Energy, Semiconductor, Data Center & Crypto")

# --- HÄR SPARAR VI DIN NYCKEL PERMANENT ---
# Radera texten 'DIN_GEMINI_NYCKEL_HÄR' och klistra in din riktiga nyckel (den som slutar på ...eM50) mellan fnuttarna.
SPARAD_GEMINI_KEY = 'DIN_GEMINI_NYCKEL_HÄR'

# --- SIDOMENY ---
st.sidebar.header("🤖 AI Inställningar")
valda_ai = st.sidebar.selectbox("Välj aktiv AI-analytiker:", ["Gemini", "Claude", "Grok"])

# Om du har sparat nyckeln ovan används den automatiskt för Gemini, annars visas textrutan
if valda_ai == "Gemini" and SPARAD_GEMINI_KEY != 'DIN_GEMINI_NYCKEL_HÄR':
    api_key = SPARAD_GEMINI_KEY
    st.sidebar.success("✅ Gemini API-nyckel laddad automatiskt!")
else:
    api_key = st.sidebar.text_input(f"{valda_ai} API-nyckel", type="password", help=f"Klistra in din {valda_ai}-nyckel.")

st.sidebar.markdown("---")

# --- REGISTER ÖVER KRYPTO ---
tillgangliga_tillgangar = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Solana (SOL)": "solana"
}

st.sidebar.header("🔍 Välj Tillgångar")
valda_namn = st.sidebar.multiselect(
    "Välj vad du vill övervaka:",
    options=list(tillgangliga_tillgangar.keys()),
    default=["Bitcoin (BTC)", "Ethereum (ETH)"]
)

# --- FUNKTION FÖR ATT HÄMTA ÄKTA LIVE-DATA ---
def hamta_live_data(crypto_id):
    try:
        # Hämtar 365 dagar av äkta historik från CoinGecko API
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=365"
        res = requests.get(url).json()
        
        priser = res['prices']
        df = pd.DataFrame(priser, columns=['Timestamp', 'Pris (USD)'])
        
        # Gör om tidsstämplar till riktiga datum
        df['Datum'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df.set_index('Datum', inplace=True)
        
        senaste_pris = round(df['Pris (USD)'].iloc[-1], 2)
        return senaste_pris, df['Pris (USD)']
    except Exception as e:
        return "N/A", None

# --- PROCESSA VARJE TILLGÅNG ---
for namn in valda_namn:
    crypto_id = tillgangliga_tillgangar[namn]
    st.markdown(f"## {namn}")
    
    col1, col2 = st.columns([2, 1])
    pris, historik_data = hamta_live_data(crypto_id)
    
    with col1:
        if historik_data is not None:
            st.metric("Senaste Pris (USD)", f"{pris:,} USD".replace(",", " "))
            st.line_chart(historik_data)
        else:
            st.error("Kunde inte ansluta till live-databasen just nu. Försök igen om en kort stund.")
            
    with col2:
        st.subheader("📰 Senaste AI Insights")
        st.write("Anslutning: 🔥 Aktiv & Realtid")
        st.caption("Analysera marknadstrender i realtid med AI.")
            
        st.markdown("---")
        st.write(f"🤖 **{valda_ai}-Analyslaboratorium**")
        
        if st.button(f"Kör {valda_ai}-analys för {namn}", key=f"btn_{crypto_id}"):
            if not api_key or api_key == 'DIN_GEMINI_NYCKEL_HÄR':
                st.warning(f"Ange en giltig API-nyckel för {valda_ai}!")
            else:
                with st.spinner(f"Ansluter till {valda_ai}..."):
                    prompt = f"Gör en kort, skarp och professionell framtidsanalys av {namn} på svenska baserat på nuvarande marknadstrender. Vad är det viktigaste att hålla koll på?"
                    
                    try:
                        if valda_ai == "Gemini":
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                            headers = {'Content-Type': 'application/json'}
                            payload = {"contents": [{"parts": [{"text": prompt}]}]}
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                            
                        elif valda_ai == "Claude":
                            url = "https://api.anthropic.com/v1/messages"
                            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
                            payload = {"model": "claude-3-5-sonnet-20241022", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]}
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['content'][0]['text'])
                            
                        elif valda_ai == "Grok":
                            url = "https://api.x.ai/v1/chat/completions"
                            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                            payload = {"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]}
                            res = requests.post(url, headers=headers, json=payload)
                            st.success(res.json()['choices'][0]['message']['content'])
                            
                    except Exception as e:
                        st.error("Kopplingen misslyckades. Dubbelkolla att din API-nyckel är rätt kopierad.")
                        
    st.markdown("---")
