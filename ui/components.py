import streamlit as st


# ============================================================
# 🚀 PREMIUM AI FINTECH HEADER
# ============================================================
def render_header(user):

    st.markdown("""
    <style>

    /* =========================
       SIDEBAR STYLING
    ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            rgba(12,18,32,0.98) 0%,
            rgba(9,14,24,0.98) 100%
        ) !important;

        border-right: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
    }

    section[data-testid="stSidebar"] * {
        color: #F5F7FA !important;
    }

    /* =========================
       NAVIGATION
    ========================= */

    div[role="radiogroup"] > label {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.04);
        padding: 12px 16px;
        border-radius: 14px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
    }

    div[role="radiogroup"] > label:hover {
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.15);
        transform: translateX(4px);
    }

    div[role="radiogroup"] > label[data-selected="true"] {
        background: linear-gradient(
            135deg,
            rgba(108,92,231,0.25) 0%,
            rgba(0,212,255,0.15) 100%
        );

        border: 1px solid rgba(0,212,255,0.25);
        box-shadow: 0 10px 30px rgba(0,212,255,0.08);
    }

    /* =========================
       USER CARD
    ========================= */

    .user-card {
        background: rgba(18,26,47,0.85);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 22px;
        padding: 18px;
        backdrop-filter: blur(16px);
        margin-top: 20px;
    }

    .user-title {
        color: #94A3B8;
        font-size: 12px;
        margin-bottom: 8px;
    }

    .user-email {
        color: white;
        font-size: 16px;
        font-weight: 700;
    }

    /* =========================
       LOGO
    ========================= */

    .logo-title {
        font-size: 30px;
        font-weight: 900;
        color: white;
        margin-bottom: 4px;
    }

    .logo-subtitle {
        color: #94A3B8;
        font-size: 13px;
        margin-bottom: 30px;
    }

    /* =========================
       BUTTON
    ========================= */

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

    # ============================================================
    # SIDEBAR
    # ============================================================

    with st.sidebar:

        # =========================
        # LOGO
        # =========================

        st.markdown("""
        <div>
            <div class="logo-title">
                🚀 CRYPTOPORT
            </div>

            <div class="logo-subtitle">
                AI Investment Intelligence Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # NAVIGATION
        # =========================

        nav = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "👤 Portfolio",
                "📈 Trading Signals",
                "🔮 Forecast",
                "⚠ Risk",
                "📉 Advanced Charts",
                "🤖 AI Assistant"
            ]
        )

        st.session_state.page = nav

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # AI STATUS CARD
        # =========================

        st.markdown("""
        <div class="user-card">

            <div style="
                color:#00D4FF;
                font-size:12px;
                font-weight:700;
                margin-bottom:12px;
            ">
                ● AI SYSTEM ONLINE
            </div>

            <div style="
                color:white;
                font-size:20px;
                font-weight:800;
                margin-bottom:8px;
            ">
                Market Status
            </div>

            <div style="
                color:#94A3B8;
                font-size:13px;
                line-height:1.6;
            ">
                Crypto market momentum remains moderately bullish.
                BTC accumulation signals detected.
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # USER CARD
        # =========================

        st.markdown(f"""
        <div class="user-card">

            <div class="user-title">
                Logged in as
            </div>

            <div class="user-email">
                👤 {user}
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

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
        font-size:28px;
        font-weight:800;
        color:white;
        margin-bottom:20px;
    ">
        💰 Live Market Overview
    </div>
    """, unsafe_allow_html=True)

    if not prices:
        st.info("⚡ Fetching live market data...")
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
                    border: 1px solid rgba(255,255,255,0.06);
                    border-radius: 24px;
                    padding: 22px;
                    backdrop-filter: blur(18px);
                    box-shadow: 0 10px 35px rgba(0,0,0,0.30);
                    transition: all 0.3s ease;
                    overflow:hidden;
                    position:relative;
                ">

                    <div style="
                        position:absolute;
                        top:-30px;
                        right:-30px;
                        width:100px;
                        height:100px;
                        background:rgba(0,212,255,0.08);
                        border-radius:50%;
                        filter: blur(20px);
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
                        font-weight:800;
                        color:white;
                        margin-bottom:12px;
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

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
