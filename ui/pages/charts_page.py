import streamlit as st
import streamlit.components.v1 as components

def render_advanced_charts():
    st.markdown("# 📉 Trading Terminal")
    
    # Selection for the trading pair
    symbol = st.selectbox(
        "Trading Pair",
        ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:XRPUSDT"]
    )

    # TradingView Widget logic
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

    # --- NEW USER EDUCATION SECTION ---
    with st.expander("📖 New to Trading? Learn how to read this chart"):
        st.write("### 🕯️ How to Read Candlesticks")
        col1, col2 = st.columns(2)
        with col1:
            st.success("**Green Candle (Bullish)**")
            st.write("The price closed **higher** than it opened. Buyers were in control during this period.")
        with col2:
            st.error("**Red Candle (Bearish)**")
            st.write("The price closed **lower** than it opened. Sellers were more aggressive during this period.")
        
        st.info("""
        **🔍 Key Elements:**
        - **The Body:** The thick part shows the price range between the 'Open' and 'Close'.
        - **The Wicks:** The thin lines above/below show the highest and lowest prices reached.
        - **Timeframe (D):** Each candle currently represents **1 Day** of trading.
        """)
