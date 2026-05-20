import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ========================================================
    # CLEAN PROFESSIONAL CSS
    # ========================================================
    st.markdown("""
    <style>
    /* 1. Eliminate all Streamlit default headers and footers */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Anchor content to the absolute top of the screen */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    /* 3. Professional White Navbar Container */
    .nav-wrapper {
        background-color: #FFFFFF;
        padding: 15px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #E2E8F0;
        position: sticky;
        top: 0;
        z-index: 9999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* 4. Sidebar Overrides for White Theme */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1E293B !important;
    }

    /* 5. Navigation Button Overrides (Invisible background) */
    div.stButton > button {
        background-color: transparent !important;
        color: #475569 !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        padding: 5px 10px !important;
        transition: color 0.3s ease !important;
    }

    div.stButton > button:hover {
        color: #3B82F6 !important;
        text-decoration: none !important;
    }

    /* Target the Active Page Button specifically */
    div.stButton > button:focus:not(:active) {
        color: #3B82F6 !important;
        border-bottom: 2px solid #3B82F6 !important;
    }

    /* 6. Professional Blue CTA Button Style */
    .cta-button {
        background-color: #3B82F6;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR LAYOUT
    # ========================================================
    # We use a wrapper div to handle the background/padding
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    
    # Columns for Logo, Nav, and Login/Status
    col_logo, col_nav, col_cta = st.columns([1.5, 6, 1.5])

    with col_logo:
        st.markdown("""
            <div style="display:flex; align-items:center;">
                <span style="font-size:24px; font-weight:800; color:#0F172A; letter-spacing:-1px;">
                    CryptoPort
                </span>
            </div>
        """, unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_cta:
        # High-contrast "Active" status or Login button look
        st.markdown("""
            <div style="display:flex; justify-content:flex-end;">
                <a class="cta-button">🟢 AI ACTIVE</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Padding for content below header
    st.markdown('<div style="height:30px"></div>', unsafe_allow_html=True)

    # Sidebar Logout and User Info
    with st.sidebar:
        st.markdown(f"### Welcome, **{user.split('@')[0]}**")
        if st.button("🚪 Logout Account", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    # Professional dark container for market data below the white header
    st.markdown("""
        <div style="padding: 0 40px;">
            <h2 style="color:#0F172A; font-weight:700; margin-bottom:20px;">Market Overview</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if prices:
        cols = st.columns(4)
        for i, (symbol, price) in enumerate(list(prices.items())[:4]):
            with cols[i]:
                st.metric(symbol, f"${price:,.2f}")
    st.markdown("---")
