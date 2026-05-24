import streamlit as st
from ui.pages.dashboard_page import render_dashboard
from ui.pages.portfolio_page import render_portfolio
from ui.pages.forecast_page import render_forecast
from ui.pages.risk_page import render_risk
from ui.pages.signals_page import render_signals
from ui.pages.charts_page import render_advanced_charts
from ui.pages.chatbot_page import render_chatbot_page

def main():
    # Fetch current page from session state
    page = st.session_state.get("page", "📊 Dashboard")
    
    # Load market data (DF) - Ensure this is defined in your app
    df = st.session_state.get("market_data") 

    # FULL PAGE ROUTING
    if page == "📊 Dashboard":
        render_dashboard(df)

    elif page == "📈 Trading Signals":
        render_signals(df)

    elif page == "📉 Advanced Charts":
        render_advanced_charts()

    elif page == "🔮 Forecast":
        render_forecast(df)

    elif page == "⚠ Risk":
        render_risk(df)

    elif page == "👤 Portfolio":
        render_portfolio(df)

    elif page == "🤖 AI Assistant":
        render_chatbot_page(df)
