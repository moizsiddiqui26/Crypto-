import streamlit as st
import time
import sys
import os

# ============================================================
# 1. CRITICAL SYSTEM PATH FIX
# ============================================================
# This ensures that 'ui', 'services', and other folders are recognized
# as modules on Streamlit Cloud, preventing the ImportError.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="🚀 CryptoPort AI Elite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 3. PROFESSIONAL UI STYLING (CSS)
# ============================================================
st.markdown("""
    <style>
        /* Hide standard Streamlit header, footer, and deploy button */
        header, footer, #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}

        /* REMOVE TEXT SELECTION TOOLBAR / DISABLE HIGHLIGHTING */
        * {
            -webkit-user-select: none; 
            -moz-user-select: none; 
            -ms-user-select: none; 
            user-select: none; 
        }

        /* Allow selection only in input fields so users can type */
        input, textarea, [data-testid="stChatInput"] {
            user-select: text !important;
            -webkit-user-select: text !important;
        }

        /* FULL PAGE LAYOUT: Remove default top padding */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Custom Scrollbar for a premium look */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f0c29;
        }
        ::-webkit-scrollbar-thumb {
            background: #00ffcc;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 4. MODULE IMPORTS
# ============================================================
try:
    from auth.auth_service import login_user, register_user
    from ui.components import render_header, render_ticker
    from ui import dashboard
    from services.live_prices import get_live_prices
    from services.alert_engine import check_alerts
    from services.email_service import send_welcome_email
    from db.database import init_db
except ImportError as e:
    st.error(f"❌ Module Error: {e}")
    st.info("Tip: Ensure you have added an empty __init__.py file inside your 'ui' folder.")
    st.stop()

# ============================================================
# 5. INITIALIZE DATABASE
# ============================================================
init_db()

# ============================================================
# 6. SESSION STATE INITIALIZATION
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
if "email" not in st.session_state:
    st.session_state.email = ""

# ============================================================
# 7. MAIN APPLICATION ENGINE
# ============================================================
def main_app():
    # Render the Professional Elite Header & Sidebar
    render_header(st.session_state.email)

    # Automated Live Price Engine (Refresh every 5 seconds)
    current_time = time.time()
    if current_time - st.session_state.last_update > 5:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time
        except Exception as e:
            print(f"Price Fetch Error: {e}")

    # Display Ticker and Check Alerts if prices exist
    if st.session_state.prices:
        render_ticker(st.session_state.prices)
        try:
            check_alerts(st.session_state.prices)
        except:
            pass

    # Feature Router: Calls the main logic in ui/dashboard.py
    # This handles Dashboard, Charts, Signals, Forecast, Risk, Portfolio, and AI
    dashboard.main()

# ============================================================
# 8. LOGIN / REGISTRATION UI
# ============================================================
def login_ui():
    st.markdown("""
        <div style="text-align:center; padding-top:60px; padding-bottom:30px;">
            <div style="font-size:52px; font-weight:900; color:white; letter-spacing:2px;">
                🚀 CRYPTOPORT
            </div>
            <div style="color:#00ffcc; font-size:18px; margin-top:5px; font-weight:600;">
                ELITE AI INTELLIGENCE
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if st.session_state.mode == "login":
            st.markdown('<h3 style="text-align:center;">🔐 Secure Login</h3>', unsafe_allow_html=True)
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("🚀 Enter Dashboard", use_container_width=True):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.success("Access Granted.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result["msg"])

            if st.button("📝 No account? Register here", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()
        else:
            # Registration UI Logic...
            st.markdown('<h3 style="text-align:center;">📝 Create Elite Account</h3>', unsafe_allow_html=True)
            # (Add registration fields as needed)
            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.mode = "login"
                st.rerun()

# ============================================================
# 9. APP ENTRY POINT
# ============================================================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
