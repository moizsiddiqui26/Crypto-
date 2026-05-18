import streamlit as st
import os
import importlib.util
import time

from dotenv import load_dotenv

# ============================================================
# LOAD ENV VARIABLES
# ============================================================

load_dotenv()

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🚀 Crypto AI Portfolio Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Branding */

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

/* Main App */

.stApp {

    background:
        radial-gradient(circle at top left,
        rgba(108,92,231,0.15),
        transparent 25%),

        radial-gradient(circle at top right,
        rgba(0,212,255,0.10),
        transparent 25%),

        linear-gradient(
            180deg,
            #081120 0%,
            #0B1020 100%
        );

    color: #F5F7FA;
}

/* Sidebar */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(10,16,32,0.98) 0%,
            rgba(5,8,18,0.98) 100%
        ) !important;

    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */

.stButton > button {

    width: 100%;

    border-radius: 14px;

    border: 1px solid rgba(255,255,255,0.08);

    background: rgba(255,255,255,0.04);

    color: white;

    font-weight: 600;

    padding: 0.8rem 1rem;

    transition: all 0.25s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    border: 1px solid rgba(0,212,255,0.20);

    background: rgba(0,212,255,0.08);
}

/* Inputs */

.stTextInput > div > div > input,
.stNumberInput input {

    background: rgba(255,255,255,0.04) !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 12px !important;

    color: white !important;
}

/* Metric Cards */

[data-testid="metric-container"] {

    background:
        linear-gradient(
            135deg,
            rgba(18,26,47,0.92) 0%,
            rgba(10,16,32,0.88) 100%
        );

    border: 1px solid rgba(255,255,255,0.06);

    padding: 20px;

    border-radius: 22px;

    backdrop-filter: blur(16px);

    box-shadow:
        0 10px 35px rgba(0,0,0,0.25);
}

/* Dataframes */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# MODULE LOADER
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_module(name, path):

    spec = importlib.util.spec_from_file_location(name, path)

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


# ============================================================
# LOAD MODULES
# ============================================================

auth = load_module(
    "auth",
    os.path.join(BASE_DIR, "auth", "auth_service.py")
)

ui = load_module(
    "ui",
    os.path.join(BASE_DIR, "ui", "components.py")
)

dashboard = load_module(
    "dashboard",
    os.path.join(BASE_DIR, "ui", "dashboard.py")
)

live_prices = load_module(
    "live_prices",
    os.path.join(BASE_DIR, "services", "live_prices.py")
)

db = load_module(
    "db",
    os.path.join(BASE_DIR, "db", "database.py")
)

alert_engine = load_module(
    "alert_engine",
    os.path.join(BASE_DIR, "services", "alert_engine.py")
)

email_service = load_module(
    "email_service",
    os.path.join(BASE_DIR, "services", "email_service.py")
)

# ============================================================
# INIT DATABASE
# ============================================================

db.init_db()

# ============================================================
# IMPORT FUNCTIONS
# ============================================================

login_user = auth.login_user
register_user = auth.register_user

render_header = ui.render_header
render_ticker = ui.render_ticker

get_live_prices = live_prices.get_live_prices

check_alerts = alert_engine.check_alerts

send_welcome_email = email_service.send_welcome_email

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
# LOGIN UI
# ============================================================

def login_ui():

    st.markdown("""
    <div style="text-align:center;padding-top:60px;padding-bottom:30px;">

        <div style="
            font-size:62px;
            font-weight:900;
            color:white;
        ">
            🚀 CRYPTOPORT
        </div>

        <div style="
            color:#94A3B8;
            font-size:18px;
            margin-top:10px;
        ">
            AI-Powered Crypto Intelligence Platform
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,4,2])

    with col2:

        # ====================================================
        # LOGIN
        # ====================================================

        if st.session_state.mode == "login":

            st.markdown("## 🔐 Login")

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            if st.button(
                "🚀 Login",
                use_container_width=True
            ):

                result = login_user(email, password)

                if result["success"]:

                    st.session_state.auth = True
                    st.session_state.email = email

                    st.success("Login successful")

                    time.sleep(1)

                    st.rerun()

                else:

                    st.error(result["msg"])

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "📝 Create Account",
                use_container_width=True
            ):

                st.session_state.mode = "register"

                st.rerun()

        # ====================================================
        # REGISTER
        # ====================================================

        else:

            st.markdown("## 📝 Create Account")

            name = st.text_input(
                "Full Name",
                placeholder="Your name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="example@gmail.com"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "✅ Register",
                use_container_width=True
            ):

                result = register_user(
                    name,
                    email,
                    password
                )

                if result["success"]:

                    st.success("Account created successfully")

                    try:

                        sent = send_welcome_email(email)

                        if sent:
                            st.success("📧 Welcome email sent")

                    except Exception as e:

                        st.warning(f"Email error: {e}")

                    time.sleep(1)

                    st.session_state.mode = "login"

                    st.rerun()

                else:

                    st.error(result["msg"])

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "⬅ Back to Login",
                use_container_width=True
            ):

                st.session_state.mode = "login"

                st.rerun()

# ============================================================
# MAIN APPLICATION
# ============================================================

def main_app():

    # ========================================================
    # HEADER
    # ========================================================

    render_header(
        st.session_state.email
    )

    # ========================================================
    # LIVE MARKET REFRESH
    # ========================================================

    current_time = time.time()

    if current_time - st.session_state.last_update > 5:

        try:

            st.session_state.prices = get_live_prices()

            st.session_state.last_update = current_time

        except Exception as e:

            st.warning(f"Market API Error: {e}")

    prices = st.session_state.prices

    # ========================================================
    # ALERT ENGINE
    # ========================================================

    if prices:

        try:

            check_alerts(prices)

        except Exception as e:

            print("Alert engine error:", e)

    # ========================================================
    # LIVE TICKER
    # ========================================================

    if prices:

        render_ticker(prices)

    else:

        with st.spinner("Fetching live market prices..."):

            time.sleep(1)

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # LOAD DASHBOARD ROUTER
    # ========================================================

    dashboard.main()

# ============================================================
# APP ROUTING
# ============================================================

if not st.session_state.auth:

    login_ui()

else:

    main_app()
