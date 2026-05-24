import streamlit as st

def render_header(user_email):
    """
    Renders a professional top navigation header with pages in the header itself.
    """

    # Initialize default page
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # Header Styling
    st.markdown("""
        <style>
            /* Main Header */
            .custom-header {
                background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
                padding: 15px 25px;
                border-radius: 0px 0px 15px 15px;
                border-bottom: 2px solid #00ffcc;
                margin-top: -65px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
            }

            /* Top Row */
            .header-top {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }

            /* Logo */
            .header-title {
                color: white;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 1.5px;
                font-family: 'Inter', sans-serif;
            }

            /* User Badge */
            .user-badge {
                background: rgba(255, 255, 255, 0.1);
                padding: 6px 14px;
                border-radius: 20px;
                color: #00ffcc;
                font-size: 13px;
                font-weight: 600;
                border: 1px solid rgba(0, 255, 204, 0.4);
                display: flex;
                align-items: center;
                gap: 8px;
            }

            /* Navigation */
            .nav-container {
                display: flex;
                gap: 10px;
                justify-content: center;
                flex-wrap: wrap;
            }

            /* Pulse Animation */
            .status-dot {
                height: 8px;
                width: 8px;
                background-color: #00ffcc;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 8px #00ffcc;
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0% {
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7);
                }
                70% {
                    transform: scale(1);
                    box-shadow: 0 0 0 10px rgba(0, 255, 204, 0);
                }
                100% {
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(0, 255, 204, 0);
                }
            }

            /* Hide Sidebar */
            section[data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header HTML
    st.markdown(f"""
        <div class="custom-header">
            <div class="header-top">
                <div class="header-title">
                    🚀 CRYPTOPORT 
                    <span style="font-size:10px; color:#94A3B8; font-weight:400; margin-left:5px;">
                        AI ELITE
                    </span>
                </div>

                <div class="user-badge">
                    <span class="status-dot"></span>
                    <span>LIVE</span> | 👤 {user_email}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Header Navigation Buttons
    nav1, nav2, nav3, nav4, nav5, nav6, nav7 = st.columns(7)

    with nav1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "📊 Dashboard"
            st.rerun()

    with nav2:
        if st.button("👤 Portfolio", use_container_width=True):
            st.session_state.page = "👤 Portfolio"
            st.rerun()

    with nav3:
        if st.button("🔮 Forecast", use_container_width=True):
            st.session_state.page = "🔮 Forecast"
            st.rerun()

    with nav4:
        if st.button("⚠ Risk", use_container_width=True):
            st.session_state.page = "⚠ Risk"
            st.rerun()

    with nav5:
        if st.button("📈 Signals", use_container_width=True):
            st.session_state.page = "📈 Trading Signals"
            st.rerun()

    with nav6:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.page = "🤖 AI Assistant"
            st.rerun()

    with nav7:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()


def render_ticker(prices):
    """
    Renders a real-time scrolling marquee ticker below the header.
    """
    if not prices:
        return

    ticker_items = ""

    for coin, details in prices.items():
        price = details['price']
        change = details['change_24h']

        color = "#00ffcc" if change >= 0 else "#ff4b4b"
        symbol = "▲" if change >= 0 else "▼"

        ticker_items += f"""
            <span style="margin-right: 40px; font-weight: bold;">
                {coin.upper()}: 
                <span style="color:white;">${price:,.2f}</span> 
                <span style="color:{color};">
                    {symbol} {abs(change):.2f}%
                </span>
            </span>
        """

    st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.3);
            padding: 10px 0;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 20px;
        ">
            <marquee scrollamount="5"
                style="
                    color: white;
                    font-family: monospace;
                    font-size: 14px;
                ">
                {ticker_items}
            </marquee>
        </div>
    """, unsafe_allow_html=True)
