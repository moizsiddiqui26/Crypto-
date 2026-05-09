import streamlit as st
import os, importlib.util
import time
from dotenv import load_dotenv

# ✅ FORCE LOAD ENV (FIX EMAIL ISSUE)
load_dotenv()

# ✅ DIRECT EMAIL IMPORT (FIX)
from services.email_service import send_welcome_email


# =========================
# 🔥 GLOBAL CSS
# =========================
st.markdown("""
<style>
/* 🚀 NEO-FINTECH UI 2026 - GLASSMORPHISM & NEON THEME */

header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div[data-testid="stToolbar"] { display: none !important; }

/* Global Background */
.stApp {
    background: radial-gradient(circle at 50% -20%, #151a30 0%, #080b14 100%);
    color: #e2e8f0;
    font-family: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
    font-weight: 400;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(15, 20, 35, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Base Glass Container */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 24px;
}
.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(0, 255, 170, 0.1);
    border: 1px solid rgba(0, 255, 170, 0.2);
}

/* Dashboard Metrics Skeleton */
.metric-container {
    padding: 15px;
}

div[data-testid="stMetricValue"] {
    font-size: 36px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #ffffff 0%, #a0aec0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

/* Premium Buttons */
.stButton>button {
    background: linear-gradient(135deg, #7000FF 0%, #00FFAA 100%);
    color: white !important;
    font-weight: 700;
    font-size: 16px;
    border-radius: 12px;
    border: none;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 10px 20px rgba(0, 255, 170, 0.2);
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(0, 255, 170, 0.4);
    filter: brightness(1.1);
}

/* Form Elements */
.stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem;
    font-size: 16px;
}
.stTextInput>div>div>input:focus {
    border-color: #00FFAA;
    box-shadow: 0 0 0 1px #00FFAA;
}

/* Neo Typography */
.section-title {
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 30px;
    background: linear-gradient(90deg, #00FFAA, #00E1FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1.5px;
}
h1, h2, h3 { font-family: 'Inter', sans-serif !important; }

/* Animations */
@keyframes skeleton-loading {
  0% { background-color: rgba(255,255,255,0.05); }
  50% { background-color: rgba(255,255,255,0.1); }
  100% { background-color: rgba(255,255,255,0.05); }
}
.skeleton {
    animation: skeleton-loading 1.5s infinite ease-in-out;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# MODULE LOADER
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =========================
# LOAD MODULES
# =========================
auth = load_module("auth", os.path.join(BASE_DIR, "auth", "auth_service.py"))
ui = load_module("ui", os.path.join(BASE_DIR, "ui", "components.py"))
live = load_module("live", os.path.join(BASE_DIR, "services", "live_prices.py"))
db = load_module("db", os.path.join(BASE_DIR, "db", "database.py"))
alert_engine = load_module("alert_engine", os.path.join(BASE_DIR, "services", "alert_engine.py"))


# =========================
# INIT DB
# =========================
db.init_db()

login_user = auth.login_user
register_user = auth.register_user

render_header = ui.render_header
render_ticker = ui.render_ticker

get_live_prices = live.get_live_prices
check_alerts = alert_engine.check_alerts


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="🚀 Crypto SaaS", layout="wide")


# =========================
# SESSION STATE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "last_update" not in st.session_state:
    st.session_state.last_update = 0

if "prices" not in st.session_state:
    st.session_state.prices = {}


# =========================
# LOGIN / REGISTER UI
# =========================
def login_ui():

    if st.session_state.auth:
        return

    st.markdown("""
    <div style="text-align:center; padding:60px;">
        <h1 style="color:#00f5ff;">🚀 Crypto SaaS</h1>
        <p style="color:gray;">Smart Crypto Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,4,2])

    with col2:

        # ================= LOGIN =================
        if st.session_state.mode == "login":

            st.markdown("### 🔐 Login")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("🚀 Login", use_container_width=True):
                res = login_user(email, password)

                if res["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.success("Login successful 🚀")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(res["msg"])

            if st.button("📝 Register", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()

        # ================= REGISTER =================
        else:

            st.markdown("### 📝 Create Account")

            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("✅ Create Account", use_container_width=True):
                res = register_user(name, email, password)

                if res["success"]:
                    st.success("Account created successfully 🎉")

                    # ================= EMAIL FIX =================
                    try:
                        email_sent = send_welcome_email(email)

                        if email_sent:
                            st.success("📧 Welcome email sent!")
                        else:
                            st.warning("⚠ Email not sent (check .env / Gmail App Password)")
                    except Exception as e:
                        st.warning(f"Email error: {e}")

                    time.sleep(1)
                    st.session_state.mode = "login"
                    st.rerun()
                else:
                    st.error(res["msg"])

            if st.button("⬅ Back to Login"):
                st.session_state.mode = "login"
                st.rerun()


# =========================
# MAIN APP
# =========================
def main_app():

    render_header(st.session_state.email)

    now = time.time()

    # ✅ CLEAN REFRESH
    if now - st.session_state.last_update > 5:
        st.session_state.prices = get_live_prices()
        st.session_state.last_update = now

    prices = st.session_state.prices

    # ================= ALERT SYSTEM =================
    if prices:
        try:
            check_alerts(prices)
        except Exception as e:
            print("Alert error:", e)

    # ================= LIVE UI =================
    if prices:
        render_ticker(prices)
    else:
        with st.spinner("⚡ Fetching live prices..."):
            time.sleep(1)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    dashboard = load_module("dashboard", os.path.join(BASE_DIR, "ui", "dashboard.py"))
    dashboard.main()


# =========================
# ROUTING
# =========================
if not st.session_state.auth:
    login_ui()
else:
    st.empty()
    main_app()
