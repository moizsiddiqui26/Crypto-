import streamlit as st


# ============================================================
# 🚀 PREMIUM MODERN HEADER + SIDEBAR
# ============================================================
def render_header(user):

    st.markdown("""
    <style>

    /* =========================================================
       REMOVE STREAMLIT DEFAULT SPACE
    ========================================================= */

    .block-container {
        padding-top: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
    }

    header {
        visibility: hidden;
        height: 0px;
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
       GLOBAL BACKGROUND
    ========================================================= */

    .stApp {

        background:
            radial-gradient(circle at top left,
            rgba(108,92,231,0.12),
            transparent 30%),

            radial-gradient(circle at top right,
            rgba(0,212,255,0.10),
            transparent 30%),

            linear-gradient(
                180deg,
                #050816 0%,
                #081120 100%
            );

        color: white;
    }

    /* =========================================================
       HEADER
    ========================================================= */

    .premium-header {

        position: sticky;

        top: 0;

        z-index: 999;

        margin-top: 0px !important;

        margin-bottom: 24px;

        padding: 18px 28px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,0.96) 0%,
                rgba(10,16,32,0.94) 100%
            );

        border: 1px solid rgba(255,255,255,0.06);

        backdrop-filter: blur(18px);

        box-shadow:
            0 10px 40px rgba(0,0,0,0.35);
    }

    /* =========================================================
       LOGO
    ========================================================= */

    .logo-title {

        font-size: 34px;

        font-weight: 900;

        color: white;

        line-height: 1;
    }

    .logo-subtitle {

        color: #94A3B8;

        font-size: 13px;

        margin-top: 6px;
    }

    /* =========================================================
       NAVIGATION
    ========================================================= */

    div[role="radiogroup"] {

        gap: 12px;

        justify-content: center;
    }

    div[role="radiogroup"] > label {

        background: rgba(255,255,255,0.03);

        border: 1px solid rgba(255,255,255,0.05);

        border-radius: 16px;

        padding: 12px 18px;

        transition: all 0.25s ease;

        min-width: 160px;

        text-align: center;
    }

    div[role="radiogroup"] > label:hover {

        transform: translateY(-2px);

        background: rgba(0,212,255,0.08);

        border: 1px solid rgba(0,212,255,0.20);
    }

    div[role="radiogroup"] > label[data-selected="true"] {

        background:
            linear-gradient(
                135deg,
                rgba(108,92,231,0.18) 0%,
                rgba(0,212,255,0.12) 100%
            );

        border: 1px solid rgba(0,212,255,0.22);

        box-shadow:
            0 8px 28px rgba(0,212,255,0.08);
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

        border-right: 1px solid rgba(255,255,255,0.05);

        width: 320px !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
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

        border: 1px solid rgba(255,255,255,0.06);

        border-radius: 24px;

        padding: 22px;

        margin-bottom: 20px;

        backdrop-filter: blur(20px);

        box-shadow:
            0 10px 35px rgba(0,0,0,0.25);
    }

    /* =========================================================
       MENU ITEMS
    ========================================================= */

    .menu-item {

        display: flex;

        align-items: center;

        gap: 12px;

        padding: 14px 16px;

        border-radius: 16px;

        margin-bottom: 10px;

        transition: all 0.25s ease;

        background: rgba(255,255,255,0.02);
    }

    .menu-item:hover {

        background: rgba(108,92,231,0.15);

        transform: translateX(4px);
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

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 22px;

        padding: 20px;
    }

    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {

        width: 100%;

        border-radius: 16px;

        border: none;

        padding: 0.9rem 1rem;

        font-weight: 700;

        font-size: 15px;

        background:
            linear-gradient(
                135deg,
                #6C5CE7 0%,
                #00D4FF 100%
            );

        color: white;

        transition: all 0.3s ease;

        box-shadow:
            0 10px 30px rgba(0,212,255,0.12);
    }

    .stButton > button:hover {

        transform: translateY(-3px);

        box-shadow:
            0 14px 40px rgba(0,212,255,0.20);
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # HEADER
    # =========================================================

    st.markdown('<div class="premium-header">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2.2, 7, 1.7])

    with col1:

        st.markdown("""
        <div class="logo-title">
            🚀 CRYPTOPORT
        </div>

        <div class="logo-subtitle">
            AI Investment Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

    with col2:

        nav = st.radio(
            "",
            [
                "📊 Dashboard",
                "👤 Portfolio",
                "📈 Trading Signals",
                "🔮 Forecast",
                "⚠ Risk",
                "📉 Advanced Charts",
                "🤖 AI Assistant"
            ],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.session_state.page = nav

    with col3:

        st.markdown(
            """
            <div style="display:flex;justify-content:flex-end;">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:8px;

                    padding:10px 16px;

                    border-radius:999px;

                    background:rgba(0,212,255,0.08);

                    border:1px solid rgba(0,212,255,0.15);

                    color:#00D4FF;

                    font-size:12px;

                    font-weight:700;
                ">

                    <div style="
                        width:8px;
                        height:8px;

                        border-radius:50%;

                        background:#00E5A8;

                        box-shadow:0 0 10px #00E5A8;
                    "></div>

                    AI SYSTEM ACTIVE

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

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
# 💰 PREMIUM LIVE TICKER
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

                    border: 1px solid rgba(255,255,255,0.06);

                    border-radius: 24px;

                    padding: 24px;

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
