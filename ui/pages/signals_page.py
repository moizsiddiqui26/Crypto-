import streamlit as st
from services.trading_signals import generate_buy_sell_signals

def render_signals(df):
    st.markdown('<div class="section-title">📈 AI Trading Signals</div>', unsafe_allow_html=True)

    # ... [Keep your previous selection and result logic here] ...

    # ==========================================
    # 📘 RSI KNOWLEDGE CENTER (Bottom Section)
    # ==========================================
    st.markdown("---")
    st.markdown("### 🎓 Understanding RSI (Relative Strength Index)")
    
    # Using columns to create a clean "Cheat Sheet"
    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        st.write("**What is RSI?**")
        st.caption("""
        The RSI is a momentum oscillator that measures the speed and change of price movements. 
        It ranges from **0 to 100**. It is primarily used to identify 'Overbought' or 'Oversold' 
        conditions in an asset.
        """)
        
    with guide_col2:
        st.write("**The Range Guide**")
        st.markdown("""
        - 🟢 **Below 30 (Oversold):** The asset may be undervalued. Potential Buying opportunity.
        - ⚪ **40 to 60 (Neutral):** Consolidation zone. No clear trend.
        - 🔴 **Above 70 (Overbought):** The asset may be overvalued. Potential Selling opportunity.
        """)

    # Visual RSI Progress Bar for the selected coin
    rsi_val = result["rsi"]
    st.write(f"**Current {coin} RSI Intensity:**")
    
    # Creating a custom progress bar color based on value
    bar_color = "green" if rsi_val < 30 else "red" if rsi_val > 70 else "blue"
    st.progress(int(rsi_val) / 100)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94A3B8;">
        <span>OVERSOLD (30)</span>
        <span style="color:{'#00ffcc' if bar_color=='green' else '#ff4b4b' if bar_color=='red' else 'white'}; 
        font-weight:bold;">CURRENT: {rsi_val:.2f}</span>
        <span>OVERBOUGHT (70)</span>
    </div>
    """, unsafe_allow_html=True)

    # Professional Note
    st.info("""
    💡 **Pro Tip:** In a strong uptrend, RSI often stays above 40 and can hit 90. 
    In a strong downtrend, it often stays below 60 and can hit 10. Always look at the 
    **Market Trend** alongside the RSI for confirmation.
    """)
