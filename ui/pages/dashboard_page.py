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
    # --- CORRELATION HEATMAP SECTION ---
    st.markdown("---")
    st.subheader("🔗 Assets Correlation Heatmap")
    
    # Calculate Correlation
    returns = filtered.pivot(index="Date", columns="Crypto", values="Close").pct_change()
    corr = returns.corr()

    # Create Heatmap
    fig2 = px.imshow(
        corr,
        text_auto=True, 
        aspect="auto",
        template="plotly_dark",
        color_continuous_scale='RdBu_r' # Red to Blue scale
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- NEW USER DESCRIPTION FOR HEATMAP ---
    with st.expander("🧩 What is a Correlation Heatmap? (New User Guide)"):
        st.markdown("""
        The **Correlation Heatmap** shows you how much different cryptocurrencies "mimic" each other's price movements.
        
        ### 🧪 How to read the numbers:
        * **$1.0$ (Perfect Correlation):** If two coins have a score of $1.0$, they move exactly the same. When one goes up, the other follows.
        * **$0.0$ (No Correlation):** The coins move independently. The price of one has no predictable effect on the other.
        * **$-1.0$ (Inverse Correlation):** The coins move in opposite directions. When one goes up, the other tends to go down.
        
        ### 💡 Why does this matter?
        * **Diversification:** If all your coins have a $0.9$ or $1.0$ correlation, your whole portfolio will drop at the same time during a crash. 
        * **Risk Management:** Investors often look for coins with **low correlation** (closer to $0$) to "spread their risk" so that if one coin performs poorly, others might stay stable.
        """)
