import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    # ========================================================
    # COINMARKETCAP MIDNIGHT UI CSS
    # ========================================================
    st.markdown("""
    <style>
    /* Hide Streamlit default components */
    [data-testid="stHeader"], #MainMenu, footer { display: none !important; }

    /* Absolute top alignment */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        background-color: #0B0E11;
    }

    /* Sticky Navbar */
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

    /* Navigation Text Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #A1A7BB !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: color 0.2s ease !important;
    }

    div.stButton > button:hover {
        color: #3861FB !important;
    }

    /* Filter Bar Styling */
    .filter-container {
        background-color: #0B0E11;
        padding: 15px 60px;
        display: flex;
        gap: 15px;
        border-bottom: 1px solid #222531;
    }
    
    .status-badge {
        background-color: rgba(56, 97, 251, 0.1);
        color: #3861FB;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR
    # ========================================================
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    col_logo, col_nav, col_auth = st.columns([1.5, 7, 1.5])

    with col_logo:
        st.markdown('<div style="font-size:20px; font-weight:800; color:white; margin-top:5px;">CryptoPort</div>', unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_auth:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.auth = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================
    # COIN FILTER BAR (Replacing Select Coin)
    # ========================================================
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    
    filter_options = ["All Assets", "BTC", "ETH", "BNB", "SOL", "XRP", "ADA"]
    
    # Create horizontal columns for filters
    f_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 5]) # Last col is spacer
    
    for i, opt in enumerate(filter_options):
        # Apply primary styling if the option is selected
        btn_type = "primary" if st.session_state.selected_coin == opt else "secondary"
        if f_cols[i].button(opt, key=f"f_{opt}", type=btn_type):
            st.session_state.selected_coin = opt
            st.rerun()

def render_ticker(prices):
    st.markdown("""
        <div style="background-color: #171924; border-bottom: 1px solid #222531; padding: 8px 60px;">
            <span style="color: #58667E; font-size: 12px; font-weight: 600;">LIVE MARKET DATA FEED</span>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(prices))
    for i, (symbol, price) in enumerate(prices.items()):
        cols[i].metric(label=symbol, value=f"${price:,.2f}")
