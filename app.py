import streamlit as st
import os
import sys

# ============================================================
# 1. FORCED SYSTEM PATH INJECTION (CRITICAL)
# ============================================================
# This ensures the folder containing app.py is recognized as a package root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

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
# 3. CSS: UI CLEANUP & DISABLE SELECTION
# ============================================================
st.markdown("""
    <style>
        /* Hide Streamlit Header/Footer */
        header, footer, #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}

        /* DISABLE TEXT SELECTION POPUP */
        * {
            -webkit-user-select: none; 
            -moz-user-select: none; 
            -ms-user-select: none; 
            user-select: none; 
        }

        /* Keep inputs selectable for typing */
        input, textarea, [data-testid="stChatInput"] {
            user-select: text !important;
            -webkit-user-select: text !important;
        }

        /* Remove top padding for full-page look */
        .block-container { padding-top: 0rem; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 4. MODULE IMPORTS WITH ERROR DIAGNOSTICS
# ============================================================
try:
    # Try importing using the root-relative path
    from ui.components import render_header, render_ticker
    from ui import dashboard
    from auth.auth_service import login_user, register_user
    from services.live_prices import get_live_prices
    from db.database import init_db
    
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.write("---")
    st.subheader("🛠️ Debugging Info for Streamlit Cloud:")
    st.write(f"**Root Directory:** `{current_dir}`")
    st.write(f"**Files Found:** `{os.listdir(current_dir)}`")
    if os.path.exists(os.path.join(current_dir, 'ui')):
        st.write(f"**Contents of /ui:** `{os.listdir(os.path.join(current_dir, 'ui'))}`")
    else:
        st.error("⚠️ The 'ui' folder was not found in the root directory!")
    st.stop()

# ============================================================
# 5. REMAINING APP LOGIC
# ============================================================
init_db()

if "auth" not in st.session_state: st.session_state.auth = False
if "page" not in st.session_state: st.session_state.page = "📊 Dashboard"

def main_app():
    render_header(st.session_state.get("email", "User"))
    # (Existing logic for price updates and ticker)
    dashboard.main()

if not st.session_state.auth:
    # Minimal Login UI for testing the fix
    st.title("🚀 CryptoPort Elite Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = login_user(email, password)
        if res["success"]:
            st.session_state.auth = True
            st.session_state.email = email
            st.rerun()
        else:
            st.error(res["msg"])
else:
    main_app()
