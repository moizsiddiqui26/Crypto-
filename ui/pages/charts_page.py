import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

def render_advanced_charts(df):
    st.markdown("# 📊 Crypto Charts & Analysis")

    # 1. Beginner-Friendly Asset Selection
    symbol_map = {
        "Bitcoin (BTC)": "BINANCE:BTCUSDT",
        "Ethereum (ETH)": "BINANCE:ETHUSDT",
        "Solana (SOL)": "BINANCE:SOLUSDT",
        "Ripple (XRP)": "BINANCE:XRPUSDT"
    }

    selected_name = st.selectbox(
        "🪙 Pick a Coin to Analyze",
        list(symbol_map.keys())
    )

    symbol = symbol_map[selected_name]

    # Extract ticker
    coin_ticker = selected_name.split("(")[1].split(")")[0]

    # Performance Section
    st.subheader(f"🌟 {selected_name} Performance at a Glance")

    coin_data = df[df["Crypto"] == coin_ticker].sort_values("Date")

    if not coin_data.empty:

        latest_price = float(coin_data.iloc[-1]["Close"])

        prev_24h = (
            float(coin_data.iloc[-2]["Close"])
            if len(coin_data) > 1
            else latest_price
        )

        prev_7d = (
            float(coin_data.iloc[-7]["Close"])
            if len(coin_data) > 7
            else latest_price
        )

        chg_24h = ((latest_price - prev_24h) / prev_24h) * 100
        chg_7d = ((latest_price - prev_7d) / prev_7d) * 100

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Current Price",
            f"${latest_price:,.2f}"
        )

        col2.metric(
            "📈 Last 24 Hours",
            f"{chg_24h:+.2f}%",
            delta=f"{chg_24h:.2f}%"
        )

        col3.metric(
            "📊 Last 7 Days",
            f"{chg_7d:+.2f}%",
            delta=f"{chg_7d:.2f}%"
        )

        if chg_7d > 5:
            st.success(
                f"🚀 {coin_ticker} has strong bullish momentum this week."
            )

        elif chg_7d < -5:
            st.error(
                f"📉 {coin_ticker} is currently experiencing a price dip."
            )

        else:
            st.info(
                f"⚖️ {coin_ticker} is moving in a relatively stable range."
            )

    else:
        st.warning("No data available for the selected coin.")

    st.markdown("---")

    # TradingView Chart
    st.subheader("🔍 Interactive TradingView Chart")

    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>

      <script
      type="text/javascript"
      src="https://s3.tradingview.com/tv.js">
      </script>

      <script type="text/javascript">
      new TradingView.widget({{
          "width": "100%",
          "height": 550,
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
      }});
      </script>
    </div>
   # ==========================
# EDUCATION & LEARNING HUB
# ==========================

st.markdown("---")
st.markdown("## 🎓 Learn Technical Analysis")

left_col, right_col = st.columns([1, 1])

# =====================================
# LEFT SIDE - BEGINNER GUIDE
# =====================================
with left_col:

    st.markdown("### 📚 Beginner's Guide")

    with st.expander("🕯️ Candlestick Basics", expanded=True):
        st.markdown("""
        ### Understanding Candlesticks

        🟢 **Green Candle**
        - Price closed higher than it opened.
        - Buyers controlled the market.

        🔴 **Red Candle**
        - Price closed lower than it opened.
        - Sellers controlled the market.

        📏 **Wicks (Shadows)**
        - Upper Wick = Highest price reached.
        - Lower Wick = Lowest price reached.

        Candlesticks help traders understand market sentiment quickly.
        """)

    with st.expander("📈 Understanding Trends"):
        st.markdown("""
        **Bullish Trend 🚀**
        - Higher highs
        - Higher lows

        **Bearish Trend 📉**
        - Lower highs
        - Lower lows

        **Sideways Market ➖**
        - Price moves in a range.
        - Market lacks direction.
        """)

    with st.expander("⚡ Volatility & Risk"):
        st.markdown("""
        **High Volatility**
        - Large price movements.
        - High risk, high reward.

        **Low Volatility**
        - Stable price movement.
        - Lower risk.
        """)

    with st.expander("💡 Beginner Trading Tips"):
        st.markdown("""
        ✅ Never invest based on one candle.

        ✅ Confirm trends using multiple candles.

        ✅ Use stop-loss to manage risk.

        ✅ Avoid emotional trading.

        ✅ Follow risk management principles.
        """)

# =====================================
# RIGHT SIDE - VIDEO LEARNING
# =====================================
with right_col:

    st.markdown("### 🎥 Video Learning Center")

    st.info(
        "Watch a beginner-friendly candlestick chart tutorial."
    )

    st.image(
        "https://img.youtube.com/vi/eynxyoKgpng/maxresdefault.jpg",
        use_container_width=True
    )

    show_video = st.button(
        "▶ Watch Candlestick Tutorial",
        use_container_width=True
    )

    if show_video:
        st.video(
            "https://www.youtube.com/watch?v=eynxyoKgpng"
        )

        st.success(
            "Use the fullscreen button in the video player for a larger view."
        )

st.markdown("---")
