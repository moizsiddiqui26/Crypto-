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
    """

    components.html(html_code, height=570)

    st.markdown("---")

    # Educational Section
    st.markdown("## 📚 Beginner's Guide")

    with st.expander("🕯️ What are Candlestick Charts?"):

        st.write("""
        Candlestick charts are used by traders to understand market
        movements and investor sentiment.

        **Green Candle**
        - Price closed higher than it opened.
        - Indicates buying pressure.

        **Red Candle**
        - Price closed lower than it opened.
        - Indicates selling pressure.

        **Wicks (Shadows)**
        - Top wick = Highest price reached.
        - Bottom wick = Lowest price reached.

        Candlesticks help traders identify trends,
        reversals, and market momentum.
        """)

    with st.expander("📉 High vs Low Volatility"):

        st.write("""
        **High Volatility**
        - Large price swings.
        - Higher risk and reward.

        **Low Volatility**
        - Smaller price movements.
        - More stable market conditions.

        Investors often use volatility to assess risk before investing.
        """)

    with st.expander("📊 How to Read Trends?"):

        st.write("""
        **Uptrend**
        - Higher highs and higher lows.
        - Indicates bullish momentum.

        **Downtrend**
        - Lower highs and lower lows.
        - Indicates bearish momentum.

        **Sideways Market**
        - Price moves within a range.
        - Indicates uncertainty in the market.
        """)

    st.markdown("---")

    # YouTube Tutorial Section
    st.subheader("🎥 Learn Candlestick Charts")

    st.info(
        "Watch this beginner-friendly video to understand how "
        "candlestick charts work and how traders analyze price action."
    )

    st.video("https://www.youtube.com/watch?v=eynxyoKgpng")

    st.success(
        "✅ After watching the video, return to the chart above and "
        "try identifying bullish and bearish candles yourself."
    )
