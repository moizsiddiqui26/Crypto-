import streamlit as st

# ======================================================
# HEADER COMPONENT
# ======================================================
def render_header(user_email):
    # Ensure current page state exists
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # 1. Custom CSS for Elite Look
    st.markdown("""
    <style>
    /* Hide Streamlit Default Sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Professional Gradient Header */
    .custom-header {
        background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
        padding: 22px 30px;
        border-radius: 0px 0px 20px 20px;
        border-bottom: 2px solid #00ffcc;
        margin-top: -75px; /* Adjust based on your layout */
        margin-bottom: 25px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.45);
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-title {
        color: white;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
    }

    .elite-tag {
        font-size: 12px;
        color: #94A3B8;
        background: rgba(148, 163, 184, 0.1);
        padding: 2px 8px;
        border-radius: 5px;
        vertical-align: middle;
        margin-left: 10px;
    }

    .user-badge {
        background: rgba(255, 255, 255, 0.08);
        padding: 8px 18px;
        border-radius: 30px;
        color: #00ffcc;
        font-size: 14px;
        border: 1px solid rgba(0, 255, 204, 0.3);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #00ffcc;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ffcc;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.5; transform: scale(0.9); }
        70% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0.5; transform: scale(0.9); }
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Render Header HTML
    # Note: Using separate string concatenation to avoid f-string syntax errors
    header_html = f"""
    <div class="custom-header">
        <div class="header-top">
            <div class="header-title">
                🚀 CRYPTOPORT <span class="elite-tag">AI ELITE</span>
            </div>
            <div class="user-badge">
                <span class="status-dot"></span>
                <span>LIVE</span>
                <span>|</span>
                <span>👤 {user_email}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # 3. Navigation Bar (Horizontal)
    cols = st.columns(7)
    menu = {
        "📊 Dashboard": "Dashboard",
        "📉 Charts": "Charts",
        "📈 Signals": "Signals",
        "🔮 Forecast": "Forecast",
        "⚠ Risk": "Risk",
        "👤 Portfolio": "Portfolio",
        "🤖 AI": "AI"
    }

    for i, (label, key) in enumerate(menu.items()):
        with cols[i]:
            # Highlight active page with a different button type
            if st.session_state.page == label:
                if st.button(label, key=f"btn_{key}", use_container_width=True, type="primary"):
                    st.session_state.page = label
                    st.rerun()
            else:
                if st.button(label, key=f"btn_{key}", use_container_width=True):
                    st.session_state.page = label
                    st.rerun()

# ======================================================
# TICKER COMPONENT
# ======================================================
def render_ticker(prices):
    if not prices:
        return

    ticker_items = ""
    for coin, details in prices.items():
        price = details["price"]
        change = details["change_24h"]
        color = "#00ffcc" if change >= 0 else "#ff4b4b"
        symbol = "▲" if change >= 0 else "▼"
        
        ticker_items += f"""
        <span style="margin-right:50px; font-weight:bold; font-family:monospace;">
            {coin.upper()}: <span style="color:white;">${price:,.2f}</span> 
            <span style="color:{color};">{symbol} {abs(change):.2f}%</span>
        </span>
        """

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.2); padding:12px 0; border-radius:10px; overflow:hidden; margin-bottom:20px; border: 1px solid rgba(255,255,255,0.05);">
        <marquee scrollamount="6" style="color: white; font-size: 15px;">
            {ticker_items}
        </marquee>
    </div>
    """, unsafe_allow_html=True)
