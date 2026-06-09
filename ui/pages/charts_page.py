import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


def render_advanced_charts(df):

    st.markdown("# 📊 Crypto Charts & Market Analysis")

    # ==========================
    # COIN SELECTION
    # ==========================
    symbol_map = {
        "Bitcoin (BTC)": "BINANCE:BTCUSDT",
        "Ethereum (ETH)": "BINANCE:ETHUSDT",
        "Solana (SOL)": "BINANCE:SOLUSDT",
        "Ripple (XRP)": "BINANCE:XRPUSDT"
    }

    selected_name = st.selectbox(
        "🪙 Select Cryptocurrency",
        list(symbol_map.keys())
    )

    symbol = symbol_map[selected_name]

    coin_ticker = selected_name.split("(")[1].split(")")[0]

    # ==========================
    # PERFORMANCE SNAPSHOT
    # ==========================
    st.subheader(f"🌟 {selected_name} Performance Snapshot")

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
                f"🚀 {coin_ticker} is showing strong bullish momentum this week."
            )

        elif chg_7d < -5:
            st.error(
                f"📉 {coin_ticker} is currently experiencing a bearish trend."
            )

        else:
            st.info(
                f"⚖️ {coin_ticker} is currently trading within a stable range."
            )

    else:
        st.warning("No data available for this cryptocurrency.")

    st.markdown("---")

    # ==========================
    # TRADINGVIEW CHART
    # ==========================
    st.subheader("📉 Interactive Trading Chart")

    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>

      <script type="text/javascript"
      src="https://s3.tradingview.com/tv.js"></script>

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
    """

    components.html(html_code, height=570)

    st.markdown("---")

    # ==========================
    # EDUCATION HUB
    # ==========================
    st.markdown("## 🎓 Learn Technical Analysis")

    left_col, right_col = st.columns([1, 1])

    # ==========================
    # LEFT SIDE
    # ==========================
    with left_col:

        st.markdown("### 📚 Beginner's Guide")

        with st.expander(
            "🕯️ Understanding Candlestick Charts",
            expanded=True
        ):

            st.markdown("""
            ### Candlestick Basics

            🟢 **Green Candle**
            - Price closed higher than opened
            - Buyers dominated

            🔴 **Red Candle**
            - Price closed lower than opened
            - Sellers dominated

            📏 **Wicks**
            - Upper wick = Highest price
            - Lower wick = Lowest price

            Candlesticks help identify market sentiment.
            """)

        with st.expander("📈 Trend Analysis"):

            st.markdown("""
            **Bullish Trend 🚀**
            - Higher highs
            - Higher lows

            **Bearish Trend 📉**
            - Lower highs
            - Lower lows

            **Sideways Market ➖**
            - Price moves within a range
            """)

        with st.expander("⚡ Volatility & Risk"):

            st.markdown("""
            **High Volatility**
            - Large price swings
            - Higher risk and reward

            **Low Volatility**
            - Smaller fluctuations
            - More stable investments
            """)

        with st.expander("💡 Trading Tips"):

            st.markdown("""
            ✅ Never trade based on a single candle.

            ✅ Always follow the trend.

            ✅ Use stop-loss protection.

            ✅ Manage risk before profit.

            ✅ Avoid emotional decisions.
            """)

    # ==========================
    # RIGHT SIDE
    # ==========================
    with right_col:

        st.markdown("### 🎥 Video Learning Center")

        st.info(
            "Watch this beginner-friendly tutorial "
            "to master candlestick charts."
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
                "Click fullscreen in the video player "
                "for a larger viewing experience."
            )

    st.markdown("---")

    st.caption(
        "📚 Educational content is for learning purposes only "
        "and should not be considered financial advice."
    )
