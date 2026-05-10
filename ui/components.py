import streamlit as st


# ============================================================
# 🚀 PREMIUM COMPONENTS FILE
# ============================================================


# ============================================================
# HEADER + PROFESSIONAL NAVBAR
# ============================================================
def render_header(user):

    st.markdown("""
    <style>

    /* =========================================================
       GLOBAL
    ========================================================= */

    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

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

    /* =========================================================
       APP BACKGROUND
    ========================================================= */

    .stApp {

        background:
            radial-gradient(circle at top left,
            rgba(108,92,231,0.10),
            transparent 30%),

            radial-gradient(circle at top right,
            rgba(0,212,255,0.08),
            transparent 30%),

            linear-gradient(
                180deg,
                #050816 0%,
                #081120 100%
            );

        color: white;
    }

    /* =========================================================
       PROFESSIONAL NAVBAR
    ========================================================= */

    .navbar-container {

        padding: 18px 28px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,0.96) 0%,
                rgba(10,16,32,0.94) 100%
            );

        border:1px solid rgba(255,255,255,0.06);

        backdrop-filter: blur(18px);

        box-shadow:
            0 10px 40px rgba(0,0,0,0.35);

        margin-bottom:24px;
    }

    /* =========================================================
       LOGO
    ========================================================= */

    .logo-main {

        font-size:32px;

        font-weight:900;

        color:white;

        line-height:1;
    }

    .logo-sub {

        color:#94A3B8;

        font-size:13px;

        margin-top:6px;
    }

    /* =========================================================
       NAV BUTTONS
    ========================================================= */

    .stButton > button {

        width:100%;

        border-radius:16px;

        border:1px solid rgba(255,255,255,0.05);

        background:rgba(255,255,255,0.03);

        color:white;

        padding:0.85rem 1rem;

        font-weight:600;

        transition:all 0.25s ease;
    }

    .stButton > button:hover {

        transform:translateY(-2px);

        background:rgba(0,212,255,0.08);

        border:1px solid rgba(0,212,255,0.18);
    }

    /* =========================================================
       AI BADGE
    ========================================================= */

    .ai-badge {

        display:flex;

        align-items:center;

        justify-content:center;

        gap:8px;

        padding:10px 16px;

        border-radius:999px;

        background:rgba(0,212,255,0.08);

        border:1px solid rgba(0,212,255,0.15);

        color:#00D4FF;

        font-size:12px;

        font-weight:700;
    }

    .ai-dot {

        width:8px;

        height:8px;

        border-radius:50%;

        background:#00E5A8;

        box-shadow:
            0 0 10px #00E5A8;
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(8,12,24,0.98) 0%,
                rgba(5,8,18,0.98) 100%
            ) !important;

        border-right:1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] * {
        color:white !important;
    }

    /* =========================================================
       SIDEBAR CARDS
    ========================================================= */

    .sidebar-card {

        background:
            linear-gradient(
                135deg,
                rgba(18,26,47,0.92) 0%,
                rgba(12,18,32,0.88) 100%
            );

        border:1px solid rgba(255,255,255,0.06);

        border-radius:24px;

        padding:22px;

        margin-bottom:20px;

        backdrop-filter: blur(20px);

        box-shadow:
            0 10px 35px rgba(0,0,0,0.25);
    }

    /* =========================================================
       USER CARD
    ========================================================= */

    .user-card {

        background:
            linear-gradient(
                135deg,
                rgba(108,92,231,0.15) 0%,
                rgba(0,212,255,0.08) 100%
            );

        border:1px solid rgba(255,255,255,0.08);

        border-radius:22px;

        padding:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # NAVBAR
    # =========================================================

    nav_items = [
        "📊 Dashboard",
        "👤 Portfolio",
        "📈 Trading Signals",
        "🔮 Forecast",
        "⚠ Risk",
        "📉 Charts",
        "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.2, 7, 1.5])

    # =========================================================
    # LOGO
    # =========================================================

    with col1:

        st.markdown("""
        <div class="logo-main">
            🚀 CRYPTOPORT
        </div>

        <div class="logo-sub">
            AI Investment Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

    # =========================================================
    # NAVIGATION
    # =========================================================

    with col2:

        menu_cols = st.columns(len(nav_items))

        for i, item in enumerate(nav_items):

            if menu_cols[i].button(item, key=f"nav_{i}"):

                st.session_state.page = item
                st.rerun()

    # =========================================================
    # AI STATUS
    # =========================================================

    with col3:

        st.markdown("""
        <div class='ai-badge'>

            <div class='ai-dot'></div>

            AI ACTIVE

        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:

        st.markdown("""
        <div style="
            font-size:34px;
            font-weight:900;
            margin-bottom:4px;
        ">
            🚀 CRYPTOPORT
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-bottom:30px;
        ">
            Premium AI Crypto Analytics
        </div>
        """, unsafe_allow_html=True)

        # =====================================================
        # MARKET STATUS
        # =====================================================

        st.markdown("""
        <div class="sidebar-card">

            <div style="
                color:#00D4FF;
                font-size:12px;
                font-weight:700;
                margin-bottom:14px;
            ">
                ● MARKET STATUS
            </div>

            <div style="
                font-size:24px;
                font-weight:800;
                margin-bottom:10px;
            ">
                Moderately Bullish
            </div>

            <div style="
                color:#94A3B8;
                font-size:13px;
                line-height:1.7;
            ">
                BTC accumulation patterns detected.
                Altcoin momentum increasing.
                Market volatility stable.
            </div>

        </div>
        """, unsafe_allow_html=True)

        # =====================================================
        # USER CARD
        # =====================================================

        st.markdown(f"""
        <div class="user-card">

            <div style="
                color:#94A3B8;
                font-size:12px;
                margin-bottom:8px;
            ">
                Logged in as
            </div>

            <div style="
                font-size:20px;
                font-weight:800;
            ">
                👤 {user}
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()


# ============================================================
# LIVE MARKET TICKER
# ============================================================
def render_ticker(prices):

    st.markdown("""
    <div style="
        font-size:34px;
        font-weight:900;
        margin-bottom:22px;
        color:white;
    ">
        💰 Live Market Overview
    </div>
    """, unsafe_allow_html=True)

    if not prices:
        st.info("Fetching live market prices...")
        return

    coins = list(prices.items())

    cols_per_row = 4

    for i in range(0, len(coins), cols_per_row):

        row = coins[i:i + cols_per_row]

        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):

            if j < len(row):

                symbol, price = row[j]

                cols[j].markdown(f"""
                <div style="

                    background:
                        linear-gradient(
                            135deg,
                            rgba(18,26,47,0.92) 0%,
                            rgba(10,16,32,0.88) 100%
                        );

                    border:1px solid rgba(255,255,255,0.06);

                    border-radius:24px;

                    padding:24px;

                    position:relative;

                    overflow:hidden;

                    backdrop-filter: blur(18px);

                    box-shadow:
                        0 10px 35px rgba(0,0,0,0.25);

                ">

                    <div style="
                        position:absolute;

                        top:-40px;
                        right:-40px;

                        width:120px;
                        height:120px;

                        background:rgba(0,212,255,0.08);

                        border-radius:50%;

                        filter: blur(24px);
                    "></div>

                    <div style="
                        color:#94A3B8;
                        font-size:13px;
                        margin-bottom:12px;
                    ">
                        {symbol}
                    </div>

                    <div style="
                        font-size:34px;
                        font-weight:900;
                        color:white;
                        margin-bottom:14px;
                    ">
                        ${price:.2f}
                    </div>

                    <div style="
                        display:inline-flex;

                        align-items:center;

                        gap:6px;

                        padding:6px 12px;

                        border-radius:999px;

                        background:rgba(0,229,168,0.10);

                        color:#00E5A8;

                        font-size:12px;

                        font-weight:700;
                    ">

                        ● LIVE MARKET

                    </div>

                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
