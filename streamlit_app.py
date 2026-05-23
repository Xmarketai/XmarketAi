import streamlit as st
import pandas as pd
import numpy as np

# Tvinga full bredd
st.set_page_config(layout="wide")

# CSS för att ta bort padding och tvinga element att expandera
st.markdown("""
    <style>
    .main > div { max-width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ XmarketAi: Stabilitetsläge")

# Data
data = {
    "Tillgång": ["BTC", "ETH", "TSLA", "NVDA", "RKLB", "VRT", "CEG", "OKLO"],
    "Pris (USD)": [76791.0, 2120.5, 426.0, 215.3, 135.7, 92.6, 225.0, 15.4]
}
df = pd.DataFrame(data)

# Visa tabell (Ingen styling, ingen krasch)
st.subheader("Marknadsdata")
st.dataframe(df, use_container_width=True)

# Grid - Inga expanderare som döljer innehåll
cols = st.columns(4)
for i, row in df.iterrows():
    with cols[i % 4]:
        st.write(f"### {row['Tillgång']}")
        st.metric("Pris", f"{row['Pris (USD)']} USD")
        # Enkel graf
        chart_data = pd.DataFrame(np.random.randn(20, 1).cumsum() + row['Pris (USD)'], columns=['Trend'])
        st.line_chart(chart_data)
