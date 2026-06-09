import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


def render_advanced_charts(df):

    st.markdown("# 📊 Crypto Charts & Market Analysis")

    # ==================================
    # COIN SELECTION
    # ==================================
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

    # ==================================
    # PERFORMANCE SNAPSHOT
    # ==================================
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
                f"⚖️ {coin_ticker} is trading within a stable range."
            )

    else:
        st.warning("No data available for the selected cryptocurrency.")

    st.markdown("---")

    # ==================================
    # TRADINGVIEW CHART
    # ==================================
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

    # ==================================
    # LEARNING CENTER
    # ==================================
    st.markdown("## 🎓 Crypto Learning Center")

    left_col, right_col = st.columns([1, 1])

    # ==================================
    # LEFT SIDE - GUIDE
    # ==================================
    with left_col:

        st.markdown("### 📚 Beginner's Guide")

        with st.expander(
            "🕯️ Understanding Candlestick Charts",
            expanded=True
        ):

            st.markdown("""
            ### Candlestick Basics

            🟢 **Green Candle**
            - Price closed higher than it opened
            - Buyers controlled the market

            🔴 **Red Candle**
            - Price closed lower than it opened
            - Sellers controlled the market

            📏 **Wicks**
            - Upper Wick = Highest price reached
            - Lower Wick = Lowest price reached

            Candlesticks help traders quickly understand market sentiment.
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
            - Price moves within a range.
            """)

        with st.expander("⚡ Volatility & Risk"):

            st.markdown("""
            **High Volatility**
            - Large price movements
            - Higher risk and reward

            **Low Volatility**
            - More stable movement
            - Lower risk
            """)

        with st.expander("💡 Beginner Trading Tips"):

            st.markdown("""
            ✅ Never trade using only one candle.

            ✅ Follow the overall trend.

            ✅ Use Stop Loss.

            ✅ Protect capital before chasing profits.

            ✅ Avoid emotional trading.
            """)

    # ==================================
    # RIGHT SIDE - VIDEO CENTER
    # ==================================
    with right_col:

        st.markdown("### 🎥 Video Learning Center")

        st.info(
            "Learn how professional traders read candlestick charts."
        )

        st.video(
            "https://www.youtube.com/watch?v=eynxyoKgpng"
        )

        st.markdown(
            """
            <div style='text-align:center; margin-top:15px;'>
                <a href='https://www.youtube.com/watch?v=eynxyoKgpng'
                   target='_blank'>
                    <button style='
                        background-color:#FF0000;
                        color:white;
                        border:none;
                        padding:12px 20px;
                        border-radius:8px;
                        font-size:16px;
                        font-weight:bold;
                        cursor:pointer;'>
                        📺 Watch on YouTube
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "💡 Use the fullscreen icon in the video player to watch in a larger view."
        )

    st.markdown("---")

    st.caption(
        "📚 Educational content is provided for learning purposes only and does not constitute financial advice."
    )
