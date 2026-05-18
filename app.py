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

st.markdown(
    """
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
    """,
    unsafe_allow_html=True)
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
