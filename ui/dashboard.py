import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from services.crypto_api import get_historical_data
from services.risk_engine import run_risk_analysis, calculate_portfolio_risk
from services.forecast_engine import get_forecast_summary
from services.ai_insights import generate_insights  # ✅ NEW
from db.models import add_holding, get_holdings


# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=300)
def load_data():
    return get_historical_data()


def space(h=25):
    st.markdown(f"<div style='height:{h}px'></div>", unsafe_allow_html=True)


# =========================
# MAIN ROUTER
# =========================
def main():
    page = st.session_state.get("page", "📊 Dashboard")
    df = load_data()

    if df is None or df.empty:
        st.error("⚠ Failed to load data")
        return

    if page == "📊 Dashboard":
        render_dashboard(df)
    elif page == "💰 Investment":
        render_investment(df)
    elif page == "⚠ Risk":
        render_risk(df)
    elif page == "🔮 Forecast":
        render_forecast(df)
    elif page == "👤 Portfolio":
        render_portfolio(df)


# ============================================================
# 📊 DASHBOARD
# ============================================================
def render_dashboard(df):

    st.markdown("### 📊 Market Overview")

    coins = sorted(df["Crypto"].unique())
    selected = st.multiselect("Select Coins", coins, default=coins[:4])

    f = df[df["Crypto"].isin(selected)].copy()

    if f.empty:
        st.warning("Select at least one coin")
        return

    # =========================
    # KPI CARDS
    # =========================
    latest = f.groupby("Crypto").last().reset_index()
    cols = st.columns(min(4, len(latest)))

    for i, row in latest.head(4).iterrows():
        price = row["Close"]

        change = f[f["Crypto"] == row["Crypto"]]["Close"].pct_change().iloc[-1]
        change = round(change * 100, 2) if pd.notna(change) else 0

        color = "#00ffcc" if change >= 0 else "#ff4b4b"

        cols[i].markdown(f"""
        <div style="
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 18px;
            border-radius: 14px;
            backdrop-filter: blur(10px);
            text-align:center;
        ">
            <div style="color:gray">{row['Crypto']}</div>
            <div style="font-size:22px;font-weight:bold;color:#00ffcc;">
                ${price:.2f}
            </div>
            <div style="color:{color}">
                {change}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    space()

    # =========================
    # DATA PREP
    # =========================
    f["Return"] = f.groupby("Crypto")["Close"].pct_change()

    pivot = f.pivot(index="Date", columns="Crypto", values="Close")
    corr = pivot.pct_change().corr()

    risk_df = run_risk_analysis(f)

    # =========================
    # 🤖 AI INSIGHTS
    # =========================
    st.markdown("### 🤖 AI Insights")

    try:
        insights = generate_insights(f, risk_df, corr)
    except Exception as e:
        insights = [f"⚠ Error generating insights: {e}"]

    for i in insights:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 8px;
        ">
            {i}
        </div>
        """, unsafe_allow_html=True)

    space()

    # =========================
    # CHARTS
    # =========================
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # PRICE TREND
    with row1_col1:
        fig1 = px.line(f, x="Date", y="Close", color="Crypto", template="plotly_dark")
        fig1.update_layout(margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig1, use_container_width=True)

    # RETURNS
    with row1_col2:
        fig2 = px.line(f, x="Date", y="Return", color="Crypto", template="plotly_dark")
        fig2.update_layout(margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # CORRELATION
    with row2_col1:
        fig3 = px.imshow(corr, text_auto=True, template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

    # DISTRIBUTION
    with row2_col2:
        fig4 = px.histogram(
            f,
            x="Return",
            color="Crypto",
            nbins=50,
            template="plotly_dark",
            opacity=0.6
        )
        st.plotly_chart(fig4, use_container_width=True)


# ============================================================
# 🔮 FORECAST (UPDATED WITH GRAPH)
# ============================================================
def render_forecast(df):

    st.markdown("### 🔮 Forecast")

    coin = st.selectbox("Select Coin", df["Crypto"].unique())
    amount = st.number_input("Investment ($)", value=1000.0)

    coin_df = df[df["Crypto"] == coin]

    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        col2.metric("Expected Value", f"${result['expected_value']:.2f}")
        col3.metric("Profit %", f"{result['profit_pct']:.2f}%")

        space()

        st.markdown("### 📈 Price Forecast")

        fig = go.Figure()

        # Historical
        fig.add_trace(go.Scatter(
            x=coin_df["Date"],
            y=coin_df["Close"],
            mode="lines",
            name="Historical"
        ))

        # Forecast
        fig.add_trace(go.Scatter(
            x=result["future_dates"],
            y=result["future_prices"],
            mode="lines+markers",
            name="Forecast"
        ))

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis_title="Date",
            yaxis_title="Price"
        )

        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# (OTHER FUNCTIONS UNCHANGED)
# ============================================================
def render_investment(df):
    st.markdown("💰 Investment Module (existing code)")


def render_risk(df):
    st.markdown("⚠ Risk Module (existing code)")


def render_portfolio(df):
    st.markdown("👤 Portfolio Module (existing code)")
