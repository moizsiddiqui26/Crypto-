import streamlit as st
import time

# 1. MUST be the first Streamlit command
st.set_page_config(
    page_title="🚀 CryptoPort AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INITIALIZE SESSION STATE IMMEDIATELY (Fixes AttributeErrors)
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
if "selected_coin" not in st.session_state:
    st.session_state.selected_coin = "All Assets"

# 3. IMPORTS
from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from services.alert_engine import check_alerts
from db.database import init_db

init_db()

def login_ui():
    st.markdown("""
        <style> .stApp { background-color: #0B0E11; } </style>
        <div style="text-align:center; padding: 80px 0 40px 0;">
            <h1 style="color:white; font-size:56px; font-weight:900;">🚀 CRYPTOPORT</h1>
            <p style="color:#94A3B8; font-size:18px;">AI-Powered Crypto Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if st.session_state.mode == "login":
            st.markdown('<h2 style="color:white; margin-bottom:20px;">🔐 Login</h2>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password")
            if st.button("🚀 Login", use_container_width=True):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error(result["msg"])
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()
        else:
            # Registration logic...
            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.mode = "login"
                st.rerun()

def main_app():
    # Renders header and the new horizontal coin selector
    render_header(st.session_state.email)

    current_time = time.time()
    if current_time - st.session_state.last_update > 5:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time
        except Exception:
            pass

    prices = st.session_state.prices
    if prices:
        check_alerts(prices)
        render_ticker(prices)

    dashboard.main()

if not st.session_state.auth:
    login_ui()
else:
    main_app()
