# ============================================================
# app.py
# COMPLETE UPDATED VERSION
# ============================================================

import streamlit as st
import time

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🚀 CryptoPort AI",
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

/* ============================================================
   HIDE STREAMLIT DEFAULT UI
============================================================ */

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

/* ============================================================
   MAIN APP BACKGROUND
============================================================ */

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

    color: white;
}

/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(8,12,24,0.98) 0%,
            rgba(5,8,18,0.98) 100%
        ) !important;

    border-right:1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color:white !important;
}

/* ============================================================
   INPUTS
============================================================ */

.stTextInput input,
.stNumberInput input {

    background: rgba(255,255,255,0.04) !important;

    border:1px solid rgba(255,255,255,0.08) !important;

    border-radius:14px !important;

    color:white !important;
}

/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {

    width:100%;

    border-radius:16px;

    border:1px solid rgba(255,255,255,0.08);

    background:rgba(255,255,255,0.04);

    color:white;

    padding:0.8rem 1rem;

    font-weight:600;

    transition:all 0.25s ease;
}

.stButton > button:hover {

    transform:translateY(-2px);

    border:1px solid rgba(0,212,255,0.20);

    background:rgba(0,212,255,0.08);
}

/* ============================================================
   METRICS
============================================================ */

[data-testid="metric-container"] {

    background:
        linear-gradient(
            135deg,
            rgba(18,26,47,0.92) 0%,
            rgba(10,16,32,0.88) 100%
        );

    border:1px solid rgba(255,255,255,0.06);

    padding:22px;

    border-radius:22px;

    backdrop-filter: blur(18px);

    box-shadow:
        0 10px 35px rgba(0,0,0,0.25);
}

/* ============================================================
   CHAT
============================================================ */

.stChatMessage {

    background: rgba(255,255,255,0.03);

    border:1px solid rgba(255,255,255,0.05);

    border-radius:20px;

    padding:12px;

    margin-bottom:12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# IMPORTS
# ============================================================

from auth.auth_service import (
    login_user,
    register_user
)

from ui.components import (
    render_header,
    render_ticker
)

from ui import dashboard

from services.live_prices import (
    get_live_prices
)

from services.alert_engine import (
    check_alerts
)

from services.email_service import (
    send_welcome_email
)

from db.database import init_db

# ============================================================
# INIT DATABASE
# ============================================================

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
# LOGIN / REGISTER UI
# ============================================================

def login_ui():

    # ========================================================
    # HERO SECTION
    # ========================================================

    st.markdown("""
    <div style="
        text-align:center;
        padding-top:60px;
        padding-bottom:30px;
    ">

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

    # ========================================================
    # LOGIN CARD
    # ========================================================

    col1, col2, col3 = st.columns([2,4,2])

    with col2:

        # ====================================================
        # LOGIN MODE
        # ====================================================

        if st.session_state.mode == "login":

            st.markdown("""
            <div style="
                font-size:42px;
                font-weight:800;
                margin-bottom:30px;
            ">
                🔐 Login
            </div>
            """, unsafe_allow_html=True)

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "🚀 Login",
                use_container_width=True
            ):

                result = login_user(
                    email,
                    password
                )

                if result["success"]:

                    st.session_state.auth = True
                    st.session_state.email = email

                    st.success(
                        "Login successful"
                    )

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
        # REGISTER MODE
        # ====================================================

        else:

            st.markdown("""
            <div style="
                font-size:42px;
                font-weight:800;
                margin-bottom:30px;
            ">
                📝 Create Account
            </div>
            """, unsafe_allow_html=True)

            name = st.text_input(
                "Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

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

                    st.success(
                        "Account created successfully"
                    )

                    try:

                        send_welcome_email(email)

                    except Exception:
                        pass

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
# MAIN APP
# ============================================================

def main_app():

    render_header(
        st.session_state.email
    )

    current_time = time.time()

    # ========================================================
    # LIVE MARKET REFRESH
    # ========================================================

    if current_time - st.session_state.last_update > 5:

        try:

            st.session_state.prices = (
                get_live_prices()
            )

            st.session_state.last_update = (
                current_time
            )

        except Exception as e:

            st.warning(
                f"Market API Error: {e}"
            )

    prices = st.session_state.prices

    # ========================================================
    # ALERTS
    # ========================================================

    if prices:

        try:

            check_alerts(prices)

        except Exception:
            pass

    # ========================================================
    # LIVE TICKER
    # ========================================================

    if prices:

        render_ticker(prices)

    else:

        with st.spinner(
            "Fetching live market prices..."
        ):

            time.sleep(1)

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # DASHBOARD ROUTER
    # ========================================================

    dashboard.main()

# ============================================================
# APP ROUTING
# ============================================================

if not st.session_state.auth:

    login_ui()

else:

    main_app()
