import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ========================================================
    # PROFESSIONAL WHITE THEME CSS
    # ========================================================
    st.markdown("""
    <style>
    /* 1. Remove Streamlit default header/footer */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Anchor content to the top of the screen */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    /* 3. Professional White Navbar */
    .nav-wrapper {
        background-color: #FFFFFF;
        padding: 15px 50px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #E2E8F0;
        position: sticky;
        top: 0;
        z-index: 9999;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* 4. Light Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #334155 !important;
    }

    /* 5. Minimalist Nav Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #64748B !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        transition: color 0.2s ease !important;
    }

    div.stButton > button:hover {
        color: #2563EB !important;
        background-color: #F1F5F9 !important;
    }

    /* 6. High-Contrast CTA (AI Active) */
    .ai-badge {
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 8px 16px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 11px;
        border: 1px solid #DBEAFE;
    }
    </style>
    """, unsafe_allow_html=True)

    # ========================================================
    # NAVBAR LAYOUT
    # ========================================================
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    
    col_logo, col_nav, col_cta = st.columns([1.5, 7, 1.5])

    with col_logo:
        st.markdown("""
            <div style="font-size:24px; font-weight:800; color:#0F172A; letter-spacing:-0.5px;">
                CryptoPort
            </div>
        """, unsafe_allow_html=True)

    with col_nav:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            # Styling active state
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()

    with col_cta:
        st.markdown('<div style="display:flex; justify-content:flex-end;"><span class="ai-badge">🟢 AI ACTIVE</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar Content
    with st.sidebar:
        st.markdown(f"### Welcome, **{user.split('@')[0]}**")
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

def render_ticker(prices):
    # Professional metrics on a light background
    st.markdown('<div style="padding: 20px 50px 0 50px;"><h3 style="color:#0F172A;">Market Watch</h3></div>', unsafe_allow_html=True)
    if prices:
        cols = st.columns(4)
        for i, (symbol, price) in enumerate(list(prices.items())[:4]):
            with cols[i]:
                st.metric(symbol, f"${price:,.2f}")
    st.markdown("<hr style='margin: 0 50px;'>", unsafe_allow_html=True)
