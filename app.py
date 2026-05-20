import streamlit as st
import time

# 1. MUST be the first Streamlit command
st.set_page_config(
    page_title="CryptoPort AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INITIALIZE SESSION STATE IMMEDIATELY (Prevents AttributeError)
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

# ============================================================
# IMPORTS
# ============================================================
from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from services.alert_engine import check_alerts
from db.database import init_db

# Initialize database
init_db()

# ============================================================
# LOGIN / REGISTER UI (Professional White Theme)
# ============================================================
def login_ui():
    st.markdown("""
        <style>
            .stApp { background-color: #FFFFFF; }
        </style>
        <div style="text-align:center; padding: 80px 0 40px 0;">
            <h1 style="color:#0F172A; font-weight:800; font-size:56px; letter-spacing:-2px;">CryptoPort</h1>
            <p style="color:#64748B; font-size:18px;">Institutional-Grade AI Crypto Analytics</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.5, 3, 2.5])
    
    with col2:
        if st.session_state.mode == "login":
            st.markdown('<h3 style="text-align:center; color:#1E293B;">Welcome Back</h3>', unsafe_allow_html=True)
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            
            if st.button("Sign In", use_container_width=True, type="primary"):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error(result["msg"])
            
            if st.button("Create an account", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()
        else:
            # Registration UI Logic here...
            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.mode = "login"
                st.rerun()

# ============================================================
# MAIN APP
# ============================================================
def main_app():
    # Render the new professional white header
    render_header(st.session_state.email)

    # Live Price logic
    current_time = time.time()
    if current_time - st.session_state.last_update > 10:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time
        except:
            pass

    if st.session_state.prices:
        check_alerts(st.session_state.prices)
        render_ticker(st.session_state.prices)

    # Load content from dashboard.py
    dashboard.main()

# ============================================================
# APP ROUTING
# ============================================================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
