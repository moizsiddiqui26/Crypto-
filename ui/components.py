import streamlit as st


def render_header(user_email):
    """
    Professional Top Navigation Header
    """

    # ---------------------------
    # Default Session State
    # ---------------------------
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ---------------------------
    # Custom CSS
    # ---------------------------
    st.markdown("""
    <style>

    /* Hide Streamlit Sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Remove Streamlit Top Padding */
    .block-container {
        padding-top: 1rem;
    }

    /* Main Header */
    .custom-header {
        background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
        padding: 18px 28px;
        border-radius: 0px 0px 18px 18px;
        border-bottom: 2px solid #00ffcc;
        margin-top: -20px;
        margin-bottom: 22px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    }

    /* Top Row */
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    /* Logo */
    .header-title {
        color: white;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* AI ELITE Tag */
    .elite-tag {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 500;
        letter-spacing: 2px;
        margin-left: 5px;
    }

    /* User Badge */
    .user-badge {
        background: rgba(255,255,255,0.08);
        padding: 10px 18px;
        border-radius: 25px;
        color: #00ffcc;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid rgba(0,255,204,0.35);
        display: flex;
        align-items: center;
        gap: 10px;
        backdrop-filter: blur(10px);
    }

    /* Live Dot */
    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #00ffcc;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ffcc;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0,255,204,0.7);
        }
        70% {
            transform: scale(1);
            box-shadow: 0 0 0 12px rgba(0,255,204,0);
        }
        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0,255,204,0);
        }
    }

    /* Navigation Buttons */
    div.stButton > button {
        background: rgba(255,255,255,0.03);
        color: white;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 10px;
        font-weight: 500;
        transition: 0.3s ease;
    }

    div.stButton > button:hover {
        border: 1px solid #00ffcc;
        color: #00ffcc;
        transform: translateY(-2px);
        box-shadow: 0px 0px 12px rgba(0,255,204,0.25);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Header HTML
    # ---------------------------
    header_html = f"""
    <div class="custom-header">

        <div class="header-top">

            <div class="header-title">
                🚀 CRYPTOPORT
                <span class="elite-tag">
                    AI ELITE
                </span>
            </div>

            <div class="user-badge">
                <span class="status-dot"></span>
                <span>LIVE</span> |
                <span>👤 {user_email}</span>
            </div>

        </div>

    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

    # ---------------------------
    # Navigation Menu
    # ---------------------------
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "📊 Dashboard"
            st.rerun()

    with col2:
        if st.button("👤 Portfolio", use_container_width=True):
            st.session_state.page = "👤 Portfolio"
            st.rerun()

    with col3:
        if st.button("🔮 Forecast", use_container_width=True):
            st.session_state.page = "🔮 Forecast"
            st.rerun()

    with col4:
        if st.button("⚠ Risk", use_container_width=True):
            st.session_state.page = "⚠ Risk"
            st.rerun()

    with col5:
        if st.button("📈 Signals", use_container_width=True):
            st.session_state.page = "📈 Trading Signals"
            st.rerun()

    with col6:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.page = "🤖 AI Assistant"
            st.rerun()

    with col7:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()


def render_ticker(prices):
    """
    Real-Time Crypto Price Ticker
    """

    if not prices:
        return

    ticker_items = ""

    for coin, details in prices.items():

        price = details["price"]
        change = details["change_24h"]

        color = "#00ffcc" if change >= 0 else "#ff4b4b"
        symbol = "▲" if change >= 0 else "▼"

        ticker_items += f"""
            <span style="margin-right:40px; font-weight:bold;">
                {coin.upper()} :
                <span style="color:white;">
                    ${price:,.2f}
                </span>

                <span style="color:{color};">
                    {symbol} {abs(change):.2f}%
                </span>
            </span>
        """

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.04);
        padding: 10px 0;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.06);
    ">

        <marquee scrollamount="5"
            style="
                color:white;
                font-family:monospace;
                font-size:14px;
            ">

            {ticker_items}

        </marquee>

    </div>
    """, unsafe_allow_html=True)
