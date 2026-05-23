import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

def render_advanced_charts(df):
    st.markdown("# 📉 Trading Terminal")

    # 1. Asset Selection
    symbol_map = {
        "Bitcoin (BTC)": "BINANCE:BTCUSDT",
        "Ethereum (ETH)": "BINANCE:ETHUSDT",
        "Solana (SOL)": "BINANCE:SOLUSDT",
        "Ripple (XRP)": "BINANCE:XRPUSDT"
    }
    
    selected_name = st.selectbox("Pick a Coin to Analyze", list(symbol_map.keys()))
    symbol = symbol_map[selected_name]
    coin_ticker = selected_name.split("(")[1].split(")")[0] # Extracts 'BTC', 'ETH', etc.

    # ---------------------------------------------------------
    # NEW: BEGINNER-FRIENDLY PERFORMANCE SNAPSHOT
    # ---------------------------------------------------------
    st.subheader(f"🌟 {selected_name} Performance at a Glance")
    
    # Filter historical data for the selected coin
    coin_data = df[df["Crypto"] == coin_ticker].sort_values("Date")
    
    if not coin_data.empty:
        latest_price = coin_data.iloc[-1]["Close"]
        
        # Calculate simple changes
        prev_24h = coin_data.iloc[-2]["Close"] if len(coin_data) > 1 else latest_price
        prev_7d = coin_data.iloc[-7]["Close"] if len(coin_data) > 7 else latest_price
        
        chg_24h = ((latest_price - prev_24h) / prev_24h) * 100
        chg_7d = ((latest_price - prev_7d) / prev_7d) * 100

        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.metric("Current Price", f"${latest_price:,.2f}")
        with c2:
            st.metric("Last 24 Hours", f"{chg_24h:+.2f}%", delta=f"{chg_24h:.2f}%")
        with c3:
            st.metric("Last 7 Days", f"{chg_7d:+.2f}%", delta=f"{chg_7d:.2f}%")

        # Beginner Friendly Interpretation
        if chg_7d > 5:
            st.success(f"🚀 **Strong Momentum:** {coin_ticker} has been growing quickly this week!")
        elif chg_7d < -5:
            st.error(f"📉 **Price Dip:** {coin_ticker} is currently cheaper than it was last week.")
        else:
            st.info(f"⚖️ **Stable:** {coin_ticker} is holding its value steadily right now.")
    
    st.markdown("---")

    # 2. Advanced TradingView Terminal
    st.subheader("🔍 Deep Dive: Interactive Chart")
    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
          "width": "100%", "height": 500, "symbol": "{symbol}",
          "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
          "style": "1", "locale": "en", "toolbar_bg": "#0B1020",
          "enable_publishing": false, "hide_side_toolbar": false,
          "allow_symbol_change": true, "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(html_code, height=520)

    # 3. Educational Guide
    with st.expander("🕯️ Beginner's Guide: How to read this graph"):
        st.write("""
        This is a **Candlestick Chart**. Each 'candle' represents one day of trading:
        - **Green Body:** The price went UP that day.
        - **Red Body:** The price went DOWN that day.
        - **Wicks (Thin Lines):** The highest and lowest points the price touched during the day.
        """)
