import streamlit as st
import streamlit.components.v1 as components

def render_advanced_charts():
    st.markdown("# 📉 Trading Terminal")

    symbol = st.selectbox(
        "Trading Pair",
        ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:XRPUSDT"]
    )

    # TradingView Terminal
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

    # --- NEW USER EDUCATION ---
    st.markdown("### 🕯️ How to Read Candlestick Charts")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **What is a Candlestick?**
        Unlike a single line, a candle shows the **High, Low, Open,** and **Close** price for a specific time period (like 1 day).
        """)
        

    with col2:
        st.success("**🟢 Green Candle**: Price ended higher than it started (Buying pressure).")
        st.error("**🔴 Red Candle**: Price ended lower than it started (Selling pressure).")

    st.info("💡 **Tip:** Each vertical bar represents **1 Day (D)** of trading. You can change this to 1 Hour (1H) using the chart's top menu.")
