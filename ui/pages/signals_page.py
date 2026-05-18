import streamlit as st

from services.trading_signals import generate_buy_sell_signals



def render_signals(df):

    st.markdown("# 📈 Trading Signals")

    coins = sorted(df["Crypto"].unique())

    coin = st.selectbox(
        "Select Coin",
        coins
    )

    coin_df = df[df["Crypto"] == coin]

    result = generate_buy_sell_signals(coin_df)

    st.metric(
        "Signal",
        result["signal"]
    )

    st.info(result["reason"])

    st.write("RSI:", result["rsi"])
    st.write("Trend:", result["trend"])
