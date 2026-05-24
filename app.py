import streamlit as st
import os
import sys

# --- FORCED PATH INJECTION ---
# This line finds the directory where app.py lives and adds it to the system path
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# ============================================================
# PAGE CONFIG (Must be the first Streamlit command)
# ============================================================
st.set_page_config(
    page_title="🚀 CryptoPort AI Elite",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# CSS: HIDE ELEMENTS & DISABLE TEXT SELECTION
# ============================================================
st.markdown("""
    <style>
        header, footer, #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        * { -webkit-user-select: none; user-select: none; }
        input, textarea, [data-testid="stChatInput"] { user-select: text !important; }
        .block-container { padding-top: 0rem; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# NOW TRY THE IMPORTS
# ============================================================
try:
    from ui.components import render_header, render_ticker
    from ui import dashboard
    from auth.auth_service import login_user, register_user
except ImportError as e:
    st.error(f"❌ Still hitting an Import Error: {e}")
    st.write(f"Current Path: {sys.path}")
    st.stop()

# ... Rest of your code below
