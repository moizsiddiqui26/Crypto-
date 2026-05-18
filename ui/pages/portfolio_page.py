import streamlit as st
import pandas as pd
import plotly.express as px

from db.models import add_holding, get_holdings



def render_portfolio(df):

    st.markdown("# 👤 Portfolio Manager")

    email = st.session_state.get("email")

    col1, col2, col3 = st.columns(3)

    coin = col1.selectbox(
        "Crypto",
        sorted(df["Crypto"].unique())
    )

    amount = col2.number_input(
        "Investment Amount",
        min_value=0.0,
        value=1000.0
    )

    date = col3.date_input("Investment Date")

    if st.button("Add Investment"):

        add_holding(
            email,
            coin,
            amount,
            str(date)
        )

        st.success("Investment Added")

    data = get_holdings(email)

    if not data:
        st.warning("No portfolio data")
        return

    portfolio = pd.DataFrame(
        data,
        columns=["Crypto", "Amount", "Date"]
    )

    st.dataframe(portfolio, use_container_width=True)

    pie = px.pie(
        portfolio,
        names="Crypto",
        values="Amount",
        template="plotly_dark"
    )

    st.plotly_chart(pie, use_container_width=True)
