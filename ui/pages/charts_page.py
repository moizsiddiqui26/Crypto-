import streamlit as st
import streamlit.components.v1 as components



def render_advanced_charts():

    st.markdown("# 📉 Trading Terminal")

    symbol = st.selectbox(
        "Trading Pair",
        [
            "BINANCE:BTCUSDT",
            "BINANCE:ETHUSDT",
            "BINANCE:SOLUSDT",
            "BINANCE:XRPUSDT"
        ]
    )

    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>

      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

      <script type="text/javascript">
      new TradingView.widget(
      {{
      "width": "100%",
      "height": 650,
      "symbol": "{symbol}",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#0B1020",
      "enable_publishing": false,
      "hide_side_toolbar": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_chart"
    }}
      );
      </script>
    </div>
    """

    components.html(html_code, height=650)
