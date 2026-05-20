import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    # ========================================================
    # CLEAN PROFESSIONAL WHITE CSS
    # ========================================================
    st.markdown("""
    <style>
    /* Force hide Streamlit default components */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* Remove the top gap */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    /* Professional White Navbar */
    .nav-wrapper {
        background-color: #FFFFFF;
        padding: 12px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #E2E8F0;
        position: sticky;
        top: 0;
        z-index: 9999;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Light Sidebar Override */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #334155 !important;
    }

    /* Text-only Nav Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #64748B !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        color: #2563EB !important;
    }

    /* AI Badge */
    .ai-badge {
        background-color: #F0F9FF;
        color: #0369A1;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 11px;
        border: 1px solid #BAE6FD;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR LAYOUT
    # ========================================================
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    
    col_logo, col_nav, col_cta = st.columns([1.5, 7, 1.5])

    with col_logo:
        st.markdown('<div style="font-size:22px; font-weight:800; color:#0F172A; margin-top:5px;">CryptoPort</div>', unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_cta:
        st.markdown('<div style="display:flex; justify-content:flex-end; margin-top:5px;"><span class="ai-badge">🟢 AI ACTIVE</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Logout
    with st.sidebar:
        st.write(f"Logged in: **{user}**")
        if st.button("🚪 Logout Account", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    st.markdown('<div style="padding: 20px 40px 0 40px;"><h3 style="color:#1E293B; font-size:20px;">Live Markets</h3></div>', unsafe_allow_html=True)
    if prices:
        cols = st.columns(4)
        for i, (symbol, price) in enumerate(list(prices.items())[:4]):
            with cols[i]:
                st.metric(symbol, f"${price:,.2f}")
    st.markdown("<hr style='margin: 0 40px; border: 0.5px solid #E2E8F0;'>", unsafe_allow_html=True)
