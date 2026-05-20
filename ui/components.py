import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    # ========================================================
    # COINMARKETCAP MIDNIGHT THEME CSS
    # ========================================================
    st.markdown("""
    <style>
    /* Hide default Streamlit overhead */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
    }

    /* Absolute top alignment */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        background-color: #0B0E11;
    }

    /* Sticky Midnight Navbar */
    .nav-wrapper {
        background-color: #171924;
        padding: 10px 60px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #222531;
        position: sticky;
        top: 0;
        z-index: 9999;
    }

    /* Sidebar CMC Style */
    section[data-testid="stSidebar"] {
        background-color: #0B0E11 !important;
        border-right: 1px solid #222531 !important;
    }

    /* Nav Item buttons disguised as text links */
    div.stButton > button {
        background-color: transparent !important;
        color: #A1A7BB !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 15px !important;
    }

    div.stButton > button:hover {
        color: #3861FB !important;
        background-color: #222531 !important;
    }

    /* Active Page Indicator (Simulated) */
    .active-nav {
        color: #3861FB !important;
        border-bottom: 2px solid #3861FB !important;
    }

    /* High Visibility Blueprint Button (CMC Style) */
    .cmc-btn {
        background-color: #3861FB;
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # HEADER LAYOUT
    # ========================================================
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    
    col_logo, col_nav, col_auth = st.columns([1.5, 7, 1.5])

    with col_logo:
        st.markdown('<div style="font-size:22px; font-weight:800; color:white; margin-top:5px;">CryptoPort</div>', unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_auth:
        st.markdown('<div style="display:flex; justify-content:flex-end; margin-top:5px;"><button class="cmc-btn">Log Out</button></div>', unsafe_allow_html=True)
        # Note: Functional logout remains in the sidebar for reliability
    
    st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"#### Account: **{user}**")
        if st.button("🚪 Sign Out"):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    # Professional horizontal ticker strip below nav
    st.markdown("""
        <div style="background-color: #171924; border-bottom: 1px solid #222531; padding: 5px 60px;">
            <span style="color: #58667E; font-size: 12px; font-weight: 600;">MARKET CAP POSITIVE</span>
        </div>
    """, unsafe_allow_html=True)
    
    if prices:
        cols = st.columns(len(prices))
        for i, (symbol, price) in enumerate(prices.items()):
            cols[i].metric(label=symbol, value=f"${price:,.2f}", delta_color="normal")
