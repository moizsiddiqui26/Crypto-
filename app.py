import streamlit as st
import os
import importlib.util
import time
from dotenv import load_dotenv

# =========================
# 🔐 LOAD ENV (IMPORTANT)
# =========================
load_dotenv()

# =========================
# 📧 EMAIL (DIRECT IMPORT)
# =========================
from services.email_service import send_welcome_email

# =========================
# 📁 MODULE LOADER
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =========================
# 🔄 LOAD MODULES
# =========================
auth = load_module("auth", os.path.join(BASE_DIR, "auth", "auth_service.py"))
ui = load_module("ui", os.path.join(BASE_DIR, "ui", "components.py"))
live = load_module("live", os.path.join(BASE_DIR, "services", "live_prices.py"))
db = load_module("db", os.path.join(BASE_DIR, "db", "database.py"))
alert_engine = load_module("alert_engine", os.path.join(BASE_DIR, "services", "alert_engine.py"))

login_user = auth.login_user
register_user = auth.register_user

render_header = ui.render_header
render_ticker = ui.render_ticker

get_live_prices = live.get_live_prices
check_alerts = alert_engine.check_alerts

# =========================
# 🗄 INIT DATABASE
# =========================
db.init_db()

# =========================
# ⚙ CONFIG
# =========================
st.set_page_config(
    page_title="🚀 CRYPTOPORT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 🎨 GLOBAL CSS (TRADING APP UI)
# =========================
st.markdown("""
<style>

/* Remove default UI */
header, #MainMenu, footer {visibility: hidden;}
div[data-testid="stToolbar"] {display: none !important;}

/* Remove spacing */
.block-container {padding-top: 0rem !important;}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #1a1840, #24243e);
    color: #eaeaf0;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00f5ff, #00ffcc);
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .block-container {
        padding: 10px !important;
    }

    h1, h2, h3 {
        font-size: 18px !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================
# 🧠 SESSION STATE
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
# 🔐 LOGIN / REGISTER
# =========================
def login_ui():

    if st.session_state.auth:
        return

    st.markdown("""
    <div style="text-align:center; padding:60px;">
        <h1 style="color:#00f5ff;">🚀 CRYPTOPORT</h1>
        <p style="color:gray;">AI-Powered Crypto Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,4,2])

    with col2:

        # LOGIN
        if st.session_state.mode == "login":

            st.markdown("### 🔐 Login")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
                res = login_user(email, password)

                if res["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.success("Login successful 🚀")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(res["msg"])

            if st.button("Create Account"):
                st.session_state.mode = "register"
                st.rerun()

        # REGISTER
        else:

            st.markdown("### 📝 Register")

            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Create Account", use_container_width=True):

                res = register_user(name, email, password)

                if res["success"]:
                    st.success("Account created 🎉")

                    # ✅ SEND WELCOME EMAIL
                    try:
                        sent = send_welcome_email(email)

                        if sent:
                            st.success("📧 Welcome email sent!")
                        else:
                            st.warning("Email not sent (check config)")
                    except Exception as e:
                        st.warning(f"Email error: {e}")

                    time.sleep(1)
                    st.session_state.mode = "login"
                    st.rerun()

                else:
                    st.error(res["msg"])

            if st.button("Back to Login"):
                st.session_state.mode = "login"
                st.rerun()


# =========================
# 🚀 MAIN APP
# =========================
def main_app():

    render_header(st.session_state.email)

    now = time.time()

    # 🔄 PRICE UPDATE
    if now - st.session_state.last_update > 5:
        st.session_state.prices = get_live_prices()
        st.session_state.last_update = now

    prices = st.session_state.prices

    # 🔔 ALERT CHECK
    if prices:
        try:
            check_alerts(prices)
        except Exception as e:
            print("Alert error:", e)

    # 💰 LIVE MARKET
    if prices:
        render_ticker(prices)
    else:
        with st.spinner("Loading market..."):
            time.sleep(1)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # 📊 LOAD DASHBOARD
    dashboard = load_module("dashboard", os.path.join(BASE_DIR, "ui", "dashboard.py"))
    dashboard.main()


# =========================
# 🔁 ROUTING
# =========================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
