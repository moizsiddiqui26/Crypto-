import streamlit as st
import time

# Set page config must be the very first command
st.set_page_config(
    page_title="🚀 CryptoPort AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# IMPORTS
# ============================================================
from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from services.alert_engine import check_alerts
from services.email_service import send_welcome_email
from db.database import init_db

# Initialize database
init_db()

# ============================================================
# SESSION STATE
# ============================================================
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
# LOGIN & REGISTRATION UI
# ============================================================
def login_ui():
    st.markdown("""
        <div style="text-align:center; padding-top:40px; padding-bottom:20px;">
            <div style="font-size:52px; font-weight:900; color:white;">🚀 CRYPTOPORT</div>
            <div style="color:#94A3B8; font-size:16px; margin-top:5px;">AI-Powered Crypto Intelligence</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        # --- LOGIN MODE ---
        if st.session_state.mode == "login":
            st.markdown('<h2 style="text-align:center;">🔐 Login</h2>', unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("🚀 Login", use_container_width=True):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    # EMAIL ALERT: Notify user of login
                    send_welcome_email(
                        email, 
                        "🚀 Security Alert: New Login detected", 
                        f"Your account was accessed on {time.strftime('%Y-%m-%d %H:%M:%S')}. If this wasn't you, please reset your password."
                    )
                    st.rerun()
                else:
                    st.error(result["msg"])
            
            if st.button("📝 Go to Registration", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()

        # --- REGISTER MODE ---
        else:
            st.markdown('<h2 style="text-align:center;">📝 Create Account</h2>', unsafe_allow_html=True)
            # FIX: Define inputs BEFORE the button is clicked
            new_email = st.text_input("Enter Email", key="reg_email")
            new_password = st.text_input("Enter Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_conf")
            
            if st.button("✅ Register Now", use_container_width=True):
                if not new_email or not new_password:
                    st.warning("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    result = register_user(new_email, new_password)
                    if result["success"]:
                        st.success("Account Created!")
                        # EMAIL ALERT: Welcome Email
                        send_welcome_email(
                            new_email, 
                            "🌟 Welcome to CryptoPort AI!", 
                            "Your account is ready. Start tracking your assets and using our AI forecasting tools now."
                        )
                        st.session_state.mode = "login"
                        st.rerun()
                    else:
                        st.error(result["msg"])
            
            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.mode = "login"
                st.rerun()

# ============================================================
# MAIN APP
# ============================================================
def main_app():
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
