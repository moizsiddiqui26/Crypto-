import streamlit as st


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="CryptoPort AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================
# HEADER COMPONENT
# ============================================
def render_header(user_email):

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ============================================
    # GLOBAL CSS
    # ============================================
    st.markdown("""
    <style>

    /* ============================================
       FULL WIDTH LAYOUT
    ============================================ */

    .main .block-container {
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* Hide Streamlit Menu + Sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    section[data-testid="stSidebar"] {
        display: none;
    }

    /* ============================================
       HEADER
    ============================================ */

    .custom-header {
        width: 100%;
        background: linear-gradient(
            135deg,
            #0f0c29,
            #302b63,
            #24243e
        );

        border-radius: 0px 0px 18px 18px;
        padding: 24px 30px;
        border-bottom: 2px solid #00ffcc;

        margin-top: -15px;
        margin-bottom: 18px;

        box-shadow: 0px 8px 30px rgba(0,0,0,0.45);
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }

    /* ============================================
       LOGO
    ============================================ */

    .header-title {
        display: flex;
        align-items: center;
        gap: 12px;

        color: white;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 1px;

        font-family: "Inter", sans-serif;
    }

    .elite-tag {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 500;
        letter-spacing: 3px;

        margin-top: 6px;
    }

    /* ============================================
       USER BADGE
    ============================================ */

    .user-badge {
        display: flex;
        align-items: center;
        gap: 10px;

        background: rgba(255,255,255,0.08);

        padding: 12px 18px;

        border-radius: 40px;

        border: 1px solid rgba(0,255,204,0.25);

        color: #00ffcc;

        font-size: 14px;
        font-weight: 600;

        backdrop-filter: blur(12px);
    }

    /* ============================================
       LIVE DOT
    ============================================ */

    .status-dot {
        width: 10px;
        height: 10px;

        border-radius: 50%;
        background: #00ffcc;

        box-shadow: 0 0 12px #00ffcc;

        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {

        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0,255,204,0.7);
        }

        70% {
            transform: scale(1);
            box-shadow: 0 0 0 12px rgba(0,255,204,0);
        }

        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0,255,204,0);
        }
    }

    /* ============================================
       NAV BUTTONS
    ============================================ */

    div.stButton > button {
        width: 100%;

        background: rgba(255,255,255,0.03);

        color: white;

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 14px;

        padding: 12px;

        font-size: 15px;
        font-weight: 500;

        transition: all 0.3s ease;
    }

    div.stButton > button:hover {

        color: #00ffcc !important;

        border: 1px solid #00ffcc !important;

        transform: translateY(-2px);

        box-shadow: 0px 0px 15px rgba(0,255,204,0.25);
    }

    /* ============================================
       MOBILE RESPONSIVE
    ============================================ */

    @media (max-width: 768px) {

        .header-title {
            font-size: 26px;
        }

        .user-badge {
            width: 100%;
            justify-content: center;
        }

    }

    </style>
    """, unsafe_allow_html=True)

    # ============================================
    # HEADER HTML
    # ============================================

    header_html = f"""
    <div class="custom-header">

        <div class="header-top">

            <div class="header-title">
                🚀 CRYPTOPORT
                <span class="elite-tag">
                    AI ELITE
                </span>
            </div>

            <div class="user-badge">
                <span class="status-dot"></span>
                <span>LIVE</span>
                <span>|</span>
                <span>👤 {user_email}</span>
            </div>

        </div>

    </div>
    """

    # IMPORTANT FIX
    st.markdown(header_html, unsafe_allow_html=True)

    # ============================================
    # NAVIGATION
    # ============================================

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c1:
        if st.button("📊 Dashboard"):
            st.session_state.page = "📊 Dashboard"
            st.rerun()

    with c2:
        if st.button("👤 Portfolio"):
            st.session_state.page = "👤 Portfolio"
            st.rerun()

    with c3:
        if st.button("🔮 Forecast"):
            st.session_state.page = "🔮 Forecast"
            st.rerun()

    with c4:
        if st.button("⚠ Risk"):
            st.session_state.page = "⚠ Risk"
            st.rerun()

    with c5:
        if st.button("📈 Signals"):
            st.session_state.page = "📈 Signals"
            st.rerun()

    with c6:
        if st.button("🤖 AI Assistant"):
            st.session_state.page = "🤖 AI Assistant"
            st.rerun()

    with c7:
        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()


# ============================================
# TICKER
# ============================================
def render_ticker(prices):

    if not prices:
        return

    ticker_items = ""

    for coin, details in prices.items():

        price = details["price"]
        change = details["change_24h"]

        color = "#00ffcc" if change >= 0 else "#ff4b4b"

        symbol = "▲" if change >= 0 else "▼"

        ticker_items += f"""
        <span style="margin-right:40px; font-weight:bold;">
            {coin.upper()}:

            <span style="color:white;">
                ${price:,.2f}
            </span>

            <span style="color:{color};">
                {symbol} {abs(change):.2f}%
            </span>
        </span>
        """

    st.markdown(f"""
    <div style="
        width:100%;
        background: rgba(255,255,255,0.04);
        padding: 12px 0;
        border-radius: 12px;
        overflow: hidden;
        margin-top: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    ">

        <marquee scrollamount="5"
            style="
                color:white;
                font-family:monospace;
                font-size:14px;
            ">

            {ticker_items}

        </marquee>

    </div>
    """, unsafe_allow_html=True)
