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
    /* Hide default Streamlit components */
    [data-testid="stHeader"], #MainMenu, footer { display: none !important; }

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

    /* CMC Link-style Navigation Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #A1A7BB !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 10px 15px !important;
        transition: color 0.2s ease !important;
    }

    div.stButton > button:hover {
        color: #3861FB !important;
    }

    /* Sidebar Dark Theme */
    section[data-testid="stSidebar"] {
        background-color: #0B0E11 !important;
        border-right: 1px solid #222531 !important;
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
    # NAVBAR LAYOUT
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
        if st.button("Log Out", key="logout_top"):
            st.session_state.auth = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================
    # HORIZONTAL COIN FILTER BAR (Reference Image Style)
    # ========================================================
    st.markdown('<div style="height:15px"></div>', unsafe_allow_html=True)
    filter_options = ["All Assets", "Bitcoin", "Ethereum", "BNB", "Solana", "XRP", "Cardano"]
    
    # Render filters as a horizontal row of buttons
    f_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 4]) # Last column is a spacer
    for i, opt in enumerate(filter_options):
        # Use primary styling for the active selection
        is_active = st.session_state.selected_coin == opt
        if f_cols[i].button(opt, key=f"filter_{opt}", type="primary" if is_active else "secondary"):
            st.session_state.selected_coin = opt
            st.rerun()

    st.markdown("<hr style='margin: 10px 60px; border: 0.1px solid #222531;'>", unsafe_allow_html=True)

def render_ticker(prices):
    # Professional ticker strip
    st.markdown("""
        <div style="background-color: #171924; border-bottom: 1px solid #222531; padding: 8px 60px;">
            <span style="color: #58667E; font-size: 11px; font-weight: 600; text-transform: uppercase;">
                Market Status: Moderately Bullish ● Live AI Monitoring Active
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    if prices:
        cols = st.columns(len(prices))
        for i, (symbol, price) in enumerate(prices.items()):
            cols[i].metric(label=symbol, value=f"${price:,.2f}")
