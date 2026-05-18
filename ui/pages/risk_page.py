import streamlit as st

from services.risk_engine import (
    run_risk_analysis,
    calculate_portfolio_risk
)



def render_risk(df):

    st.markdown("# ⚠ Portfolio Risk Analysis")

    risk_df = run_risk_analysis(df)

    st.dataframe(risk_df, use_container_width=True)

    portfolio = calculate_portfolio_risk(df)

    col1, col2 = st.columns(2)

    col1.metric(
        "Risk Level",
        portfolio["level"]
    )

    col2.metric(
        "Risk Score",
        portfolio["score"]
    )
