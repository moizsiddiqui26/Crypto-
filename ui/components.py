import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    # Global CSS for Midnight Theme and Layout
    st.markdown("""
    <style>
    [data-testid="stHeader"], #MainMenu, footer { display: none !important; }
    .block-container {
        padding-top: 0rem !important;
        background-color: #0B0E11 !important;
    }
    .nav-wrapper {
        background-color: #171924;
        padding: 15px 40px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #222531;
        position: sticky;
        top: 0;
        z-index: 9999;
    }
    div.stButton > button {
        background-color: transparent !important;
        color: #A1A7BB !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    div.stButton > button:hover {
        color: #3861FB !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Navbar Container
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 7, 1.5])
    
    with col1:
        st.markdown('<div style="font-size:24px; font-weight:900; color:white;">🚀 CRYPTOPORT</div>', unsafe_allow_html=True)
    
    with col2:
        nav_cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            if nav_cols[i].button(item, key=f"nav_{i}"):
                st.session_state.page = item
                st.rerun()
                
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # HORIZONTAL COIN FILTER BAR
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    filter_options = ["All Assets", "Bitcoin", "Ethereum", "BNB", "Solana", "XRP", "Cardano"]
    
    f_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 4]) 
    for i, opt in enumerate(filter_options):
        # Apply primary styling for the selected filter
        is_active = st.session_state.selected_coin == opt
        if f_cols[i].button(opt, key=f"f_{opt}", type="primary" if is_active else "secondary"):
            st.session_state.selected_coin = opt
            st.rerun()

    st.markdown("<hr style='margin: 10px 40px; border: 0.1px solid #222531;'>", unsafe_allow_html=True)

def render_ticker(prices):
    # Professional market data strip
    st.markdown('<div style="padding: 0 40px;"><h3 style="color:white;">Live Market Feed</h3></div>', unsafe_allow_html=True)
    if prices:
        cols = st.columns(len(prices))
        for i, (symbol, price) in enumerate(prices.items()):
            cols[i].metric(label=symbol, value=f"${price:,.2f}")
