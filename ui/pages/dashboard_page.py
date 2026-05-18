import streamlit as st
import plotly.express as px
import pandas as pd


def render_dashboard(df):

    st.markdown("# 📊 Market Dashboard")

    coins = sorted(df["Crypto"].unique())

    selected = st.multiselect(
        "Select Coins",
        coins,
        default=coins[:4]
    )

    filtered = df[df["Crypto"].isin(selected)]

    if filtered.empty:
        st.warning("Select at least one coin")
        return

    latest = filtered.groupby("Crypto").last().reset_index()

    cols = st.columns(min(4, len(latest)))

    for i, row in latest.head(4).iterrows():

        cols[i].metric(
            row["Crypto"],
            f"${row['Close']:.2f}"
        )

    fig = px.line(
        filtered,
        x="Date",
        y="Close",
        color="Crypto",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    returns = filtered.pivot(
        index="Date",
        columns="Crypto",
        values="Close"
    ).pct_change()

    corr = returns.corr()

    fig2 = px.imshow(
        corr,
        text_auto=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)