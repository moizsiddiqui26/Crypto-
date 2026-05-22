import streamlit as st
import streamlit.components.v1 as components

def render_advanced_charts():
    st.markdown("# 📉 Trading Terminal")
    
    # Selection for the trading pair
    symbol = st.selectbox(
        "Trading Pair",
        ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:XRPUSDT"]
    )

    # TradingView Widget
    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
          "width": "100%", "height": 650, "symbol": "{symbol}",
          "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
          "style": "1", "locale": "en", "toolbar_bg": "#0B1020",
          "enable_publishing": false, "hide_side_toolbar": false,
          "allow_symbol_change": true, "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(html_code, height=650)

    # --- NEW USER CANDLESTICK GUIDE ---
    st.markdown("---")
    st.subheader("🕯️ Candlestick Guide for Beginners")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **What are these 'Candles'?**
        Unlike a simple line, each 'candle' on this chart tells you 4 things:
        1. **Open:** The price when the time period started.
        2. **High:** The highest price reached.
        3. **Low:** The lowest price reached.
        4. **Close:** The price when the time period ended.
        """)
        
    with col2:
        st.success("**🟢 Green Candle (Bullish)**")
        st.write("The price finished higher than it started. Buyers are winning.")
        
        st.error("**🔴 Red Candle (Bearish)**")
        st.write("The price finished lower than it started. Sellers are in control.")

    st.warning("💡 **Pro Tip:** Each candle represents **1 Day (D)** of time. You can change this using the top toolbar in the chart to see 1-hour or 1-week views!")
