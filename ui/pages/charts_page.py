import streamlit as st
import streamlit.components.v1 as components

def render_advanced_charts():
    st.markdown("# 📉 Trading Terminal")
    symbol = st.selectbox("Trading Pair", ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT"])

    # TradingView Widget
    html_code = f"""
    <div id="tradingview_chart"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
        "width": "100%", "height": 500, "symbol": "{symbol}",
        "interval": "D", "theme": "dark", "container_id": "tradingview_chart"
    }});
    </script>
    """
    components.html(html_code, height=520)

    st.subheader("🕯️ Understanding Candlesticks")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**🟢 Green (Bullish):** Price went up. Buyers are stronger.")
    with col2:
        st.error("**🔴 Red (Bearish):** Price went down. Sellers are stronger.")
