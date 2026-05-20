import streamlit as st
import time

# 1. Page Config
st.set_page_config(
    page_title="CryptoPort | Portfolio Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FIX: Initialize Session State BEFORE anything else
if "auth" not in st.session_state:
    st.session_state.auth = False
if "mode" not in st.session_state:
    st.session_state.mode = "login"
if "prices" not in st.session_state:
    st.session_state.prices = {}
if "last_update" not in st.session_state:
    st.session_state.last_update = 0
if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"

# Imports
from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from db.database import init_db

init_db()

# ============================================================
# LOGIN UI (CoinMarketCap Dark Style)
# ============================================================
def login_ui():
    st.markdown("""
        <style> .stApp { background-color: #0B0E11; } </style>
        <div style="text-align:center; padding: 100px 0 30px 0;">
            <h1 style="color:white; font-size:44px; font-weight:800;">Sign Up Today</h1>
            <p style="color:#A1A7BB; font-size:20px;">Keep track of your profits and portfolio valuation.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    with col2:
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Create your Portfolio", type="primary", use_container_width=True):
            result = login_user(email, password)
            if result["success"]:
                st.session_state.auth = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error(result["msg"])

# ============================================================
# MAIN APPLICATION
# ============================================================
def main_app():
    render_header(st.session_state.email)

    # Refresh live prices
    curr = time.time()
    if curr - st.session_state.last_update > 10:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = curr
        except: pass

    if st.session_state.prices:
        render_ticker(st.session_state.prices)

    dashboard.main()

# Routing
if not st.session_state.auth:
    login_ui()
else:
    main_app()
