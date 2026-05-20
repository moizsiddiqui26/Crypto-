import streamlit as st
import time

# MUST be the first line
st.set_page_config(
    page_title="CryptoPort AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# REMOVED: Legacy components.html block that caused the spillage bug

from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from services.alert_engine import check_alerts
from db.database import init_db

init_db()

# Session State Initialization (Keep your existing session state logic here...)

def login_ui():
    # Updated Login UI to match the light professional theme
    st.markdown("""
        <div style="text-align:center; padding: 100px 0 50px 0;">
            <h1 style="color:#0F172A; font-weight:800; font-size:48px;">CryptoPort</h1>
            <p style="color:#64748B; font-size:18px;">The Enterprise AI Crypto Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    with col2:
        with st.form("login_form"):
            st.subheader("Login to your account")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                # Login logic...
                pass

def main_app():
    # Renders the new white-themed professional header
    render_header(st.session_state.email)

    # Market data logic...
    prices = st.session_state.prices
    if prices:
        render_ticker(prices)

    dashboard.main()

if not st.session_state.auth:
    login_ui()
else:
    main_app()
