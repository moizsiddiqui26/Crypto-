import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ========================================================
    # COINMARKETCAP MIDNIGHT THEME CSS
    # ========================================================
    st.markdown("""
    <style>
    /* 1. Hide default Streamlit overhead */
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
        background-color: #0B0E11; /* CMC Background */
    }

    /* 3. Sticky Midnight Navbar */
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

    /* 4. Sidebar Styles */
    section[data-testid="stSidebar"] {
        background-color: #0B0E11 !important;
        border-right: 1px solid #222531 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #CFD6E4 !important;
    }

    /* 5. CMC Link-style Navigation Buttons */
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
        color: #3861FB !important; /* CMC Primary Blue */
        background-color: transparent !important;
    }

    /* 6. Professional Blue Badge */
    .status-badge {
        background-color: rgba(56, 97, 251, 0.1);
        color: #3861FB;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 11px;
        border: 1px solid rgba(56, 97, 251, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR LAYOUT
    # ========================================================
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    
    col_logo, col_nav, col_cta = st.columns([1.5, 7, 1.5])

    with col_logo:
        st.markdown('<div style="font-size:22px; font-weight:800; color:white; margin-top:5px;">CryptoPort</div>', unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_cta:
        st.markdown('<div style="display:flex; justify-content:flex-end; margin-top:5px;"><span class="status-badge">🟢 AI ACTIVE</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Logout and Info
    with st.sidebar:
        st.markdown(f"#### Logged in as: **{user}**")
        if st.button("🚪 Logout Account", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    # Secondary ticker row below the main header
    st.markdown("""
        <div style="background-color: #171924; border-bottom: 1px solid #222531; padding: 8px 60px;">
            <span style="color: #58667E; font-size: 12px; font-weight: 600; text-transform: uppercase;">
                Market Data Live Update
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    if prices:
        cols = st.columns(len(prices))
        for i, (symbol, price) in enumerate(prices.items()):
            with cols[i]:
                st.metric(label=symbol, value=f"${price:,.2f}")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
