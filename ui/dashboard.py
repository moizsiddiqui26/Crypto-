import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from services.crypto_api import get_historical_data
from services.risk_engine import run_risk_analysis, calculate_portfolio_risk
from services.forecast_engine import get_forecast_summary
from services.ai_portfolio import optimize_portfolio
from services.ai_signals import generate_signals
from services.ai_openai import get_ai_response

from db.models import add_holding, get_holdings
from services.email_service import send_portfolio_summary_email


# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=300)
def load_data():
    return get_historical_data()


# =========================
# MAIN ENTRY
# =========================
def main():

    page = st.session_state.get("page", "📊 Market")
    df = load_data()

    if df is None or df.empty:
        st.error("⚠ Failed to load data")
        return

    if page == "📊 Market":
        render_market(df)

    elif page == "💰 AI Portfolio":
        render_ai_portfolio(df)

    elif page == "⚠ Risk":
        render_risk(df)

    elif page == "🔮 AI Forecast":
        render_forecast(df)

    elif page == "👤 Portfolio":
        render_portfolio(df)

    elif page == "🤖 AI":
        render_ai_chat(df)


# ============================================================
# 📊 MARKET (TRADING VIEW STYLE)
# ============================================================
def render_market(df):

    st.markdown("## 📊 Market Overview")

    # 🔥 MARKET TABLE
    latest = df.groupby("Crypto").last().reset_index()

    latest["Change %"] = (
        df.groupby("Crypto")["Close"].pct_change().groupby(df["Crypto"]).last().values * 100
    )

    st.dataframe(
        latest[["Crypto", "Close", "Change %"]]
        .rename(columns={"Close": "Price"}),
        use_container_width=True
    )

    st.markdown("### 📈 Candlestick Chart")

    coin = st.selectbox("Select Coin", df["Crypto"].unique())
    coin_df = df[df["Crypto"] == coin]

    fig = go.Figure(data=[go.Candlestick(
        x=coin_df["Date"],
        open=coin_df["Close"],
        high=coin_df["Close"] * 1.02,
        low=coin_df["Close"] * 0.98,
        close=coin_df["Close"]
    )])

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # ================= AI SIGNALS =================
    st.markdown("### 🧠 AI Buy/Sell Signals")

    signals = generate_signals(df)
    st.dataframe(signals, use_container_width=True)


# ============================================================
# 💰 AI PORTFOLIO
# ============================================================
def render_ai_portfolio(df):

    st.markdown("## 🤖 AI Portfolio Allocation")

    amount = st.number_input("Investment ($)", value=1000.0)

    if st.button("Generate AI Portfolio"):

        result = optimize_portfolio(df, amount)

        if result.empty:
            st.warning("No valid portfolio")
            return

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(result, use_container_width=True)

        with col2:
            fig = px.pie(result, names="Crypto", values="Investment", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ⚠ RISK
# ============================================================
def render_risk(df):

    st.markdown("## ⚠ Risk Analysis")

    risk_df = run_risk_analysis(df)
    st.dataframe(risk_df, use_container_width=True)

    portfolio = calculate_portfolio_risk(df)

    col1, col2 = st.columns(2)
    col1.metric("Risk Level", portfolio["level"])
    col2.metric("Risk Score", portfolio["score"])


# ============================================================
# 🔮 AI FORECAST
# ============================================================
def render_forecast(df):

    st.markdown("## 🔮 AI Forecast")

    coin = st.selectbox("Select Coin", df["Crypto"].unique())
    amount = st.number_input("Investment ($)", value=1000.0)

    coin_df = df[df["Crypto"] == coin]

    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        col1, col2, col3 = st.columns(3)

        col1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        col2.metric("Expected Value", f"${result['expected_value']:.2f}")
        col3.metric("Profit %", f"{result['profit_pct']:.2f}%")


# ============================================================
# 👤 PORTFOLIO
# ============================================================
def render_portfolio(df):

    st.markdown("## 👤 Portfolio")

    email = st.session_state.get("email")

    col1, col2, col3 = st.columns(3)
    coin = col1.selectbox("Crypto", df["Crypto"].unique())
    amount = col2.number_input("Amount ($)", min_value=0.0)
    date = col3.date_input("Date")

    if st.button("Add Investment"):
        add_holding(email, coin, amount, str(date))
        st.success("Added!")

    data = get_holdings(email)

    if not data:
        st.info("No investments yet")
        return

    portfolio_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

    latest_prices = df.groupby("Crypto").last().reset_index()[["Crypto", "Close"]]
    latest_prices.rename(columns={"Close": "Current Price"}, inplace=True)

    portfolio_df = portfolio_df.merge(latest_prices, on="Crypto", how="left")

    portfolio_df["Quantity"] = portfolio_df["Amount"] / portfolio_df["Current Price"]
    portfolio_df["Current Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]
    portfolio_df["Profit ($)"] = portfolio_df["Current Value"] - portfolio_df["Amount"]

    st.dataframe(portfolio_df, use_container_width=True)

    if st.button("📧 Send Portfolio Email"):
        send_portfolio_summary_email(email, portfolio_df)
        st.success("Email sent!")


# ============================================================
# 🤖 AI CHAT (OPENAI)
# ============================================================
def render_ai_chat(df):

    st.markdown("## 🤖 CRYPTOPORT AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask about crypto...")

    if user_input:

        latest = df.groupby("Crypto").last().reset_index()
        context = latest.to_string(index=False)

        response = get_ai_response(user_input, context)

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("ai", response))

    for role, msg in st.session_state.chat_history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg)
