import streamlit as st

from services.forecast_engine import get_forecast_summary



def render_forecast(df):

    st.markdown("# 🔮 AI Forecast")

    coin = st.selectbox(
        "Select Coin",
        sorted(df["Crypto"].unique())
    )

    amount = st.number_input(
        "Investment",
        value=1000.0
    )

    coin_df = df[df["Crypto"] == coin]

    result = get_forecast_summary(
        coin_df,
        amount,
        7
    )

    if result:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Predicted Price",
            f"${result['predicted_price']:.2f}"
        )

        col2.metric(
            "Expected Value",
            f"${result['expected_value']:.2f}"
        )

        col3.metric(
            "Profit %",
            f"{result['profit_pct']:.2f}%"
        )
