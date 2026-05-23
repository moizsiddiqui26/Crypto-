import streamlit as st
import plotly.express as px

def render_dashboard(df):
    st.markdown("# 📊 Market Dashboard")
    
    # ... (Keep existing filtering and metric code) ...

    st.subheader("📈 Price Trend History")
    fig = px.line(df, x="Date", y="Close", color="Crypto", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Educational Guide
    with st.expander("📖 New User: How to read this chart"):
        st.write("This line graph tracks the value of assets over time. The **Vertical Axis (Y)** is the price, and the **Horizontal Axis (X)** is time. Moving upward indicates a 'Bullish' trend (growth).")

    st.subheader("🔗 Assets Correlation Heatmap")
    # ... (Keep existing correlation math) ...
    
    with st.expander("🧩 Understanding Correlation"):
        st.markdown("""
        The Heatmap shows how coins move together:
        * **1.0**: Move in perfect sync.
        * **0.0**: No relationship.
        * **Diversification Tip:** Try to pick assets with lower correlation scores to reduce portfolio risk.
        """)
