import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ========================================================
    # GLOBAL CSS
    # ========================================================
    st.markdown("""
    <style>
    /* 1. Hide the default Streamlit header and footer */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Remove the default top padding to set project header at top */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Navbar styling */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 999;
        background: linear-gradient(135deg, rgba(15,23,42,0.96) 0%, rgba(10,16,32,0.94) 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 24px;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8,12,24,0.98) 0%, rgba(5,8,18,0.98) 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.18);
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR CONTAINER
    # ========================================================
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2.5, 6, 1.5])

    with col1:
        st.markdown("""
        <div style="font-size:32px; font-weight:900; color:white;">🚀 CRYPTOPORT</div>
        <div style="color:#94A3B8; font-size:13px; margin-top:6px;">AI Investment Intelligence Platform</div>
        """, unsafe_allow_html=True)

    with col2:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col3:
        # Fixed "AI ACTIVE" to prevent raw code leak
        st.markdown("""
        <div style="
            display:flex; align-items:center; justify-content:center;
            padding:10px 14px; border-radius:999px;
            background:rgba(0,212,255,0.08); border:1px solid rgba(0,212,255,0.18);
            color:#00D4FF; font-size:12px; font-weight:700; white-space:nowrap;
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
        <div style="font-size:34px; font-weight:900; margin-bottom:6px; color:white;">🚀 CRYPTOPORT</div>
        <div style="color:#94A3B8; font-size:13px; margin-bottom:28px;">Premium AI Crypto Analytics</div>
        """, unsafe_allow_html=True)

        # Market Status Card
        st.markdown("""
        <div style="background:rgba(18,26,47,0.92); border:1px solid rgba(255,255,255,0.06); border-radius:24px; padding:22px; margin-bottom:20px;">
            <div style="color:#00D4FF; font-size:12px; font-weight:700; margin-bottom:14px;">● MARKET STATUS</div>
            <div style="font-size:20px; font-weight:800; color:white;">Moderately Bullish</div>
        </div>
        """, unsafe_allow_html=True)

        # User Card
        st.markdown(f"""
        <div style="background:rgba(108,92,231,0.15); border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:20px; margin-bottom:20px;">
            <div style="color:#94A3B8; font-size:12px; margin-bottom:8px;">Logged in as</div>
            <div style="font-size:16px; font-weight:800; color:white; word-wrap:break-word;">👤 {user}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    st.markdown('<div style="font-size:34px; font-weight:900; margin-bottom:24px; color:white;">💰 Live Market Overview</div>', unsafe_allow_html=True)
    if not prices:
        st.info("Fetching live market prices...")
        return

    coins = list(prices.items())
    cols_per_row = 4
    for i in range(0, len(coins), cols_per_row):
        row = coins[i:i + cols_per_row]
        cols = st.columns(cols_per_row)
        for j, (symbol, price) in enumerate(row):
            cols[j].metric(symbol, f"${price:.2f}")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
