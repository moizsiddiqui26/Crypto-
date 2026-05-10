import streamlit as st


# ============================================================
# 🚀 PREMIUM HEADER + SIDEBAR
# ============================================================
def render_header(user):

    st.markdown("""
    <style>

    /* =========================================================
       GLOBAL
    ========================================================= */

    header {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* =========================================================
       TOP HEADER
    ========================================================= */

    .top-header {
        position: sticky;
        top: 0;
        z-index: 999;
        padding: 14px 24px;
        margin-bottom: 18px;

        background: rgba(10,16,32,0.78);

        border: 1px solid rgba(255,255,255,0.06);

        border-radius: 22px;

        backdrop-filter: blur(20px);

        box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    }

    .header-title {
        font-size: 30px;
        font-weight: 900;
        color: white;
    }

    .header-subtitle {
        color: #94A3B8;
        font-size: 13px;
        margin-top: 3px;
    }

    .header-ai-status {
        display: inline-block;

        padding: 8px 14px;

        border-radius: 999px;

        background: rgba(0,212,255,0.10);

        color: #00D4FF;

        font-size: 12px;
        font-weight: 700;
    }

    /* =========================================================
       NAVIGATION TABS
    ========================================================= */

    div[role="radiogroup"] {
        gap: 10px;
    }

    div[role="radiogroup"] > label {
        background: rgba(255,255,255,0.03);

        border: 1px solid rgba(255,255,255,0.05);

        padding: 10px 14px;

        border-radius: 14px;

        transition: all 0.25s ease;
    }

    div[role="radiogroup"] > label:hover {
        background: rgba(0,212,255,0.08);

        border: 1px solid rgba(0,212,255,0.20);

        transform: translateY(-2px);
    }

    div[role="radiogroup"] > label[data-selected="true"] {
        background: linear-gradient(
            135deg,
            rgba(108,92,231,0.20) 0%,
            rgba(0,212,255,0.12) 100%
        );

        border: 1px solid rgba(0,212,255,0.25);

        box-shadow: 0 8px 24px rgba(0,212,255,0.08);
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {

        background: linear-gradient(
            180deg,
            rgba(10,16,32,0.98) 0%,
            rgba(8,12,24,0.98) 100%
        ) !important;

        border-right: 1px solid rgba(255,255,255,0.06);

        backdrop-filter: blur(20px);
    }

    section[data-testid="stSidebar"] * {
        color: #F5F7FA !important;
    }

    /* =========================================================
       SIDEBAR CARDS
    ========================================================= */

    .sidebar-card {

        background: rgba(18,26,47,0.82);

        border: 1px solid rgba(255,255,255,0.05);

        border-radius: 22px;

        padding: 20px;

        backdrop-filter: blur(18px);

        margin-bottom: 20px;
    }

    .sidebar-title {
        color: white;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .sidebar-text {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.6;
    }

    /* =========================================================
       BUTTON
    ========================================================= */

    .stButton > button {

        width: 100%;

        border-radius: 14px;

        border: none;

        padding: 0.85rem 1rem;

        background: linear-gradient(
            135deg,
            #6C5CE7 0%,
            #00D4FF 100%
        );

        color: white;

        font-weight: 700;

        transition: all 0.3s ease;
    }

    .stButton > button:hover {

        transform: translateY(-3px);

        box-shadow: 0 12px 30px rgba(0,212,255,0.20);
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # HEADER
    # =========================================================

    st.markdown("""
    <div class="top-header">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,6,2])

    with col1:

        st.markdown("""
        <div class="header-title">
            🚀 CRYPTOPORT
        </div>

        <div class="header-subtitle">
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

        st.markdown("""
        <div style="text-align:right;">
            <div class="header-ai-status">
                ● AI SYSTEM ACTIVE
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:

        # =========================
        # LOGO
        # =========================

        st.markdown("""
        <div style="
            font-size:30px;
            font-weight:900;
            color:white;
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

        # =========================
        # MARKET STATUS
        # =========================

        st.markdown("""
        <div class="sidebar-card">

            <div style="
                color:#00D4FF;
                font-size:12px;
                font-weight:700;
                margin-bottom:12px;
            ">
                ● LIVE MARKET STATUS
            </div>

            <div class="sidebar-title">
                AI Market Insight
            </div>

            <div class="sidebar-text">
                Bitcoin accumulation signals detected.
                Market momentum remains moderately bullish.
                Risk conditions currently stable.
            </div>

        </div>
        """, unsafe_allow_html=True)

        # =========================
        # QUICK STATS
        # =========================

        st.markdown("""
        <div class="sidebar-card">

            <div class="sidebar-title">
                📈 Market Metrics
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-top:15px;
            ">
                <div>
                    <div style="color:#94A3B8;font-size:12px;">
                        Sentiment
                    </div>

                    <div style="
                        color:#00E5A8;
                        font-weight:800;
                        margin-top:4px;
                    ">
                        Bullish
                    </div>
                </div>

                <div>
                    <div style="color:#94A3B8;font-size:12px;">
                        Fear & Greed
                    </div>

                    <div style="
                        color:white;
                        font-weight:800;
                        margin-top:4px;
                    ">
                        72
                    </div>
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)

        # =========================
        # USER CARD
        # =========================

        st.markdown(f"""
        <div class="sidebar-card">

            <div style="
                color:#94A3B8;
                font-size:12px;
                margin-bottom:8px;
            ">
                Logged in as
            </div>

            <div style="
                color:white;
                font-size:18px;
                font-weight:800;
            ">
                👤 {user}
            </div>

        </div>
        """, unsafe_allow_html=True)

        # =========================
        # LOGOUT
        # =========================

        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()


# ============================================================
# 💰 PREMIUM LIVE TICKER
# ============================================================
def render_ticker(prices):

    st.markdown("""
    <div style="
        font-size:30px;
        font-weight:900;
        color:white;
        margin-bottom:20px;
    ">
        💰 Live Market Overview
    </div>
    """, unsafe_allow_html=True)

    if not prices:
        st.info("⚡ Fetching live market prices...")
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
                    background: rgba(18,26,47,0.82);

                    border: 1px solid rgba(255,255,255,0.05);

                    border-radius: 24px;

                    padding: 22px;

                    backdrop-filter: blur(20px);

                    box-shadow: 0 10px 35px rgba(0,0,0,0.30);

                    position:relative;

                    overflow:hidden;
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
                        margin-bottom:10px;
                    ">
                        {symbol}
                    </div>

                    <div style="
                        font-size:30px;
                        font-weight:900;
                        color:white;
                        margin-bottom:14px;
                    ">
                        ${price:.2f}
                    </div>

                    <div style="
                        display:inline-block;

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
