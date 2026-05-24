import streamlit as st
import time

# ============================================================
# PAGE CONFIG
# ============================================================
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

# ============================================================
# INITIALIZE DATABASE
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

if "email" not in st.session_state:
    st.session_state.email = ""

if "name" not in st.session_state:
    st.session_state.name = ""

# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #000428, #004e92);
    color: white;
}

div[data-testid="stForm"] {
    background-color: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 15px;
}

.stTextInput input {
    background-color: #1e1e2f;
    color: white;
    border-radius: 10px;
    border: 1px solid #555;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #0072ff, #00c6ff);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOGIN / REGISTER UI
# ============================================================
def login_ui():

    # ========================================================
    # HEADER
    # ========================================================
    st.markdown(
        """
        <div style="text-align:center; padding-top:40px; padding-bottom:20px;">
            
            <h1 style="
                font-size:60px;
                font-weight:900;
                color:white;
                margin-bottom:10px;
            ">
                🚀 CRYPTOPORT
            </h1>

            <p style="
                color:#CBD5E1;
                font-size:18px;
                margin-top:0px;
            ">
                AI-Powered Crypto Intelligence
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        # ====================================================
        # LOGIN MODE
        # ====================================================
        if st.session_state.mode == "login":

            st.markdown(
                """
                <h2 style='text-align:center; color:white;'>
                    🔐 Login
                </h2>
                """,
                unsafe_allow_html=True
            )

            email = st.text_input(
                "Email",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_pass"
            )

            if st.button("🚀 Login"):

                if not email or not password:
                    st.warning("Please fill all fields.")

                else:

                    try:
                        result = login_user(email, password)

                        if result["success"]:

                            st.session_state.auth = True
                            st.session_state.email = email

                            if "user" in result:
                                st.session_state.name = result["user"]["name"]

                            st.success("✅ Login Successful")

                            time.sleep(1)

                            st.rerun()

                        else:
                            st.error(result["msg"])

                    except Exception as e:
                        st.error(f"Login Error: {e}")

            if st.button("📝 Create Account"):
                st.session_state.mode = "register"
                st.rerun()

        # ====================================================
        # REGISTER MODE
        # ====================================================
        else:

            st.markdown(
                """
                <h2 style='text-align:center; color:white;'>
                    📝 Create Account
                </h2>
                """,
                unsafe_allow_html=True
            )

            new_name = st.text_input(
                "Full Name",
                key="reg_name"
            )

            new_email = st.text_input(
                "Email",
                key="reg_email"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="reg_pass"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="reg_conf"
            )

            if st.button("✅ Register"):

                # =================================================
                # VALIDATION
                # =================================================
                if not new_name or not new_email or not new_password:
                    st.warning("Please fill all fields.")

                elif new_password != confirm_password:
                    st.error("Passwords do not match.")

                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")

                else:

                    try:

                        result = register_user(
                            new_name,
                            new_email,
                            new_password
                        )

                        if result["success"]:

                            st.success("✅ Account Created Successfully")

                            # Send welcome email
                            try:
                                send_welcome_email(new_email)
                            except Exception as e:
                                print("Email Error:", e)

                            time.sleep(1)

                            st.session_state.mode = "login"

                            st.rerun()

                        else:
                            st.error(result["msg"])

                    except Exception as e:
                        st.error(f"Registration Error: {e}")

            if st.button("⬅ Back to Login"):
                st.session_state.mode = "login"
                st.rerun()

# ============================================================
# MAIN APPLICATION
# ============================================================
def main_app():

    try:
        render_header(st.session_state.email)

    except Exception as e:
        st.error(f"Header Error: {e}")

    current_time = time.time()

    # ========================================================
    # AUTO PRICE REFRESH
    # ========================================================
    if current_time - st.session_state.last_update > 5:

        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time

        except Exception as e:
            print("Price Fetch Error:", e)

    prices = st.session_state.prices

    # ========================================================
    # ALERTS + TICKER
    # ========================================================
    if prices:

        try:
            check_alerts(prices)
        except Exception as e:
            print("Alert Engine Error:", e)

        try:
            render_ticker(prices)
        except Exception as e:
            print("Ticker Error:", e)

    # ========================================================
    # DASHBOARD
    # ========================================================
    try:
        dashboard.main()

    except Exception as e:
        st.error(f"Dashboard Error: {e}")

# ============================================================
# APP ENTRY
# ============================================================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
