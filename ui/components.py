import streamlit as st
def render_header(user):

    nav_items = [
        "📊 Dashboard",
        "👤 Portfolio",
        "📈 Trading Signals",
        "🔮 Forecast",
        "⚠ Risk",
        "📉 Advanced Charts",
        "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ========================================================
    # GLOBAL CSS
    # ========================================================

    st.markdown("""
    <style>

    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* =====================================================
       NAVBAR
    ===================================================== */

    .navbar {

        background:
            linear-gradient(
                135deg,
                rgba(15,23,42,0.96) 0%,
                rgba(10,16,32,0.94) 100%
            );

        border:1px solid rgba(255,255,255,0.06);

        border-radius:24px;

        padding:22px;

        margin-bottom:24px;

        backdrop-filter: blur(18px);

        box-shadow:
            0 10px 35px rgba(0,0,0,0.25);
    }

    /* =====================================================
       SIDEBAR
    ===================================================== */

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

    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton > button {

        width:100%;

        border-radius:14px;

        border:1px solid rgba(255,255,255,0.06);

        background:rgba(255,255,255,0.03);

        color:white;

        font-weight:600;

        padding:0.75rem 1rem;

        transition:all 0.25s ease;
    }

    .stButton > button:hover {

        transform:translateY(-2px);

        background:rgba(0,212,255,0.08);

        border:1px solid rgba(0,212,255,0.18);
    }

    /* =====================================================
       METRIC CARDS
    ===================================================== */

    [data-testid="metric-container"] {

        background:
            linear-gradient(
                135deg,
                rgba(18,26,47,0.92) 0%,
                rgba(10,16,32,0.88) 100%
            );

        border:1px solid rgba(255,255,255,0.06);

        padding:20px;

        border-radius:22px;

        backdrop-filter: blur(18px);
    }

    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR CONTAINER
    # ========================================================

    st.markdown(
        '<div class="navbar">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2, 7, 1.5])

    # ========================================================
    # LOGO
    # ========================================================

    with col1:

        st.markdown("""
        <div style="
            font-size:32px;
            font-weight:900;
            color:white;
        ">
            🚀 CRYPTOPORT
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-top:6px;
        ">
            AI Investment Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # NAVIGATION
    # ========================================================

    with col2:

        nav_cols = st.columns(len(nav_items))

        for i, item in enumerate(nav_items):

            if nav_cols[i].button(
                item,
                key=f"nav_{i}"
            ):

                st.session_state.page = item
                st.rerun()

    # ========================================================
    # AI STATUS
    # ========================================================

    with col3:

        st.markdown("""
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;

            padding:10px 14px;

            border-radius:999px;

            background:rgba(0,212,255,0.08);

            border:1px solid rgba(0,212,255,0.18);

            color:#00D4FF;

            font-size:12px;
            font-weight:700;
        ">
            🟢 AI ACTIVE
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown("""
        <div style="
            font-size:34px;
            font-weight:900;
            margin-bottom:6px;
        ">
            🚀 CRYPTOPORT
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-bottom:28px;
        ">
            Premium AI Crypto Analytics
        </div>
        """, unsafe_allow_html=True)

        # ====================================================
        # MARKET STATUS
        # ====================================================

        st.markdown("""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    rgba(18,26,47,0.92) 0%,
                    rgba(10,16,32,0.88) 100%
                );

            border:1px solid rgba(255,255,255,0.06);

            border-radius:24px;

            padding:22px;

            margin-bottom:20px;
        ">

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
                BTC accumulation patterns detected.<br>
                Altcoin momentum increasing.<br>
                Market volatility stable.
            </div>

        </div>
        """, unsafe_allow_html=True)

        # ====================================================
        # USER CARD
        # ====================================================

        st.markdown(f"""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    rgba(108,92,231,0.15) 0%,
                    rgba(0,212,255,0.08) 100%
                );

            border:1px solid rgba(255,255,255,0.08);

            border-radius:22px;

            padding:20px;

            margin-bottom:20px;
        ">

            <div style="
                color:#94A3B8;
                font-size:12px;
                margin-bottom:8px;
            ">
                Logged in as
            </div>

            <div style="
                font-size:18px;
                font-weight:800;
                word-wrap:break-word;
            ">
                👤 {user}
            </div>

        </div>
        """, unsafe_allow_html=True)

        # ====================================================
        # LOGOUT
        # ====================================================

        if st.button("🚪 Logout"):

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
        margin-bottom:24px;
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

                cols[j].metric(
                    symbol,
                    f"${price:.2f}"
                )

        st.markdown(
            "<div style='height:12px'></div>",
            unsafe_allow_html=True
        )
