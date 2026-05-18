import streamlit as st

from services.crypto_api import get_historical_data

from ui.pages.dashboard_page import render_dashboard
from ui.pages.portfolio_page import render_portfolio
from ui.pages.forecast_page import render_forecast
from ui.pages.risk_page import render_risk
from ui.pages.signals_page import render_signals
from ui.pages.charts_page import render_advanced_charts
from ui.pages.chatbot_page import render_chatbot_page


@st.cache_data(ttl=300)
def load_data():
    return get_historical_data()



def main():

    page = st.session_state.get("page", "📊 Dashboard")

    df = load_data()

    if df is None or df.empty:
        st.error("Failed to load data")
        return

    if page == "📊 Dashboard":
        render_dashboard(df)

    elif page == "👤 Portfolio":
        render_portfolio(df)

    elif page == "🔮 Forecast":
        render_forecast(df)

    elif page == "⚠ Risk":
        render_risk(df)

    elif page == "📈 Trading Signals":
        render_signals(df)

    elif page == "📉 Advanced Charts":
        render_advanced_charts()

    elif page == "🤖 AI Assistant":
        render_chatbot_page(df)
