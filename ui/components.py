import streamlit as st

def render_header(user):
    nav_items = [
        "📊 Dashboard", "👤 Portfolio", "📈 Trading Signals", 
        "🔮 Forecast", "⚠ Risk", "📉 Advanced Charts", "🤖 AI Assistant"
    ]

    # Professional CSS injection
    st.markdown("""
    <style>
    /* Hide Streamlit elements */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
    }

    /* Set project header at top */
    .block-container {
        padding-top: 0rem !important;
        max-width: 100% !important;
    }

    .navbar {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }

    .ai-badge {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        color: #00d4ff;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Navbar Container
    with st.container():
        # Using a single row for a professional horizontal header
        col1, col2, col3 = st.columns([1.5, 7, 1.5])
        
        with col1:
            st.markdown('<h3 style="margin:0; color:white;">🚀 CRYPTOPORT</h3>', unsafe_allow_html=True)
            
        with col2:
            nav_cols = st.columns(len(nav_items))
            for i, item in enumerate(nav_items):
                # Highlight active page button
                is_active = st.session_state.page == item
                if nav_cols[i].button(item, key=f"nav_{i}", type="primary" if is_active else "secondary"):
                    st.session_state.page = item
                    st.rerun()

        with col3:
            st.markdown('<div class="ai-badge">🟢 AI ACTIVE</div>', unsafe_allow_html=True)

    st.sidebar.markdown(f"**User:** {user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.auth = False
        st.rerun()

def render_ticker(prices):
    # Standard ticker logic...
    st.markdown('<div style="height:1px; background:rgba(255,255,255,0.1); margin: 20px 0;"></div>', unsafe_allow_html=True)
    cols = st.columns(len(prices))
    for i, (symbol, price) in enumerate(prices.items()):
        cols[i].metric(symbol, f"${price:,.2f}")
