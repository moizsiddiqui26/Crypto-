import streamlit as st
import plotly.express as px
import pandas as pd

def render_dashboard(df):
    st.markdown("# 📊 Market Dashboard")

    # Selection Logic
    coins = sorted(df["Crypto"].unique())
    selected = st.multiselect("Select Coins", coins, default=coins[:4])
    filtered = df[df["Crypto"].isin(selected)]

    if filtered.empty:
        st.warning("Select at least one coin")
        return

    # Metrics Row
    latest = filtered.groupby("Crypto").last().reset_index()
    cols = st.columns(min(4, len(latest)))

    for i, row in latest.head(4).iterrows():
        cols[i].metric(row["Crypto"], f"${row['Close']:.2f}")

    # Main Price Chart
    st.subheader("📈 Price Trend History")
    fig = px.line(filtered, x="Date", y="Close", color="Crypto", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # --- NEW USER EDUCATION ---
    with st.expander("📖 New User Guide: How to read this Dashboard"):
        st.write("### 🔍 Understanding the Visuals")
        st.write("""
        * **The Line Chart**: Shows the price journey over time. A line moving **upwards** indicates increasing market value (Bullish).
        * **Timeline (X-Axis)**: Shows the date range. Moving left to right shows the history of the asset.
        * **Price (Y-Axis)**: Shows the value in USD.
        * **Correlation Heatmap (Below)**: Shows how coins move in relation to each other. A score close to **1.0** means they move almost identically.
        """)

    # Correlation Heatmap
    returns = filtered.pivot(index="Date", columns="Crypto", values="Close").pct_change()
    corr = returns.corr()
    fig2 = px.imshow(corr, text_auto=True, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)
