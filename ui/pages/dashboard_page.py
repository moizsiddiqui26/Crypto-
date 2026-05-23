import streamlit as st
import plotly.express as px
import pandas as pd

def render_dashboard(df):
    st.markdown("# 📊 Market Dashboard")
    
    # Selection & Filtering
    coins = sorted(df["Crypto"].unique())
    selected = st.multiselect("Select Coins", coins, default=coins[:4])
    filtered = df[df["Crypto"].isin(selected)]

    # Metrics
    latest = filtered.groupby("Crypto").last().reset_index()
    cols = st.columns(min(4, len(latest)))
    for i, row in latest.head(4).iterrows():
        cols[i].metric(row["Crypto"], f"${row['Close']:.2f}")

    # Chart
    st.subheader("📈 Price Trend History")
    fig = px.line(filtered, x="Date", y="Close", color="Crypto", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("❓ How to read the Price Chart"):
        st.write("The line chart shows price movement over time. An upward slope means the asset is gaining value. The X-axis is time, and the Y-axis is the price in USD.")

    # Correlation Heatmap
    st.subheader("🔗 Assets Correlation Heatmap")
    returns = filtered.pivot(index="Date", columns="Crypto", values="Close").pct_change()
    corr = returns.corr()
    fig2 = px.imshow(corr, text_auto=True, template="plotly_dark", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("🧩 Understanding Correlation (New User Guide)"):
        st.markdown("""
        * **1.0 (Same):** Coins move together. High risk if they both drop.
        * **0.0 (Independent):** No relationship between their prices.
        * **-1.0 (Opposite):** When one goes up, the other goes down.
        * **Why it matters:** Diversity! Try to hold assets that don't all move in perfect sync to protect your portfolio.
        """)
