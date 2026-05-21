import streamlit as st
import time

# 1. Page Config (Must be first)
st.set_page_config(
    page_title="CryptoPort | AI Portfolio Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Initialize Session State BEFORE imports or logic
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"
if "selected_coin" not in st.session_state:
    st.session_state.selected_coin = "All Assets"
if "prices" not in st.session_state:
    st.session_state.prices = {}
if "last_update" not in st.session_state:
    st.session_state.last_update = 0

# 3. Imports
from auth.auth_service import login_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from db.database import init_db

init_db()

def login_ui():
    st.markdown("""
        <style> .stApp { background-color: #0B0E11; } </style>
        <div style="text-align:center; padding: 100px 0 40px 0;">
            <h1 style="color:white; font-size:48px; font-weight:800;">Sign In to CryptoPort</h1>
            <p style="color:#A1A7BB; font-size:18px;">Access institutional AI crypto intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    with col2:
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Access Dashboard", type="primary", use_container_width=True):
            result = login_user(email, password)
            if result["success"]:
                st.session_state.auth = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error(result["msg"])

def main_app():
    # Render the new CoinMarketCap style header
    render_header(st.session_state.get("email", "User"))

    # Data Refresh Logic
    current_time = time.time()
    if current_time - st.session_state.last_update > 10:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time
        except: pass

    if st.session_state.prices:
        render_ticker(st.session_state.prices)

    # Route to dashboard.py
    dashboard.main()

# Routing logic
if not st.session_state.auth:
    login_ui()
else:
    main_app()
