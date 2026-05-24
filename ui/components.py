import streamlit as st

def render_header(user_email):
    """
    Renders the professional Elite header and Sidebar Navigation.
    """
    # 1. CSS for Complete Page Styling & Header
    st.markdown("""
        <style>
            /* Remove standard Streamlit padding for a 'Full Page' feel */
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            
            /* Professional Gradient Header */
            .custom-header {
                background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
                padding: 15px 30px;
                border-radius: 0px 0px 15px 15px;
                border-bottom: 2px solid #00ffcc;
                margin-top: -10px; 
                margin-bottom: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
            }
            
            .header-title {
                color: white; font-size: 26px; font-weight: 800; letter-spacing: 1.5px;
            }
            
            .user-badge {
                background: rgba(255, 255, 255, 0.1);
                padding: 8px 16px;
                border-radius: 30px;
                color: #00ffcc;
                font-size: 13px;
                border: 1px solid rgba(0, 255, 204, 0.5);
                display: flex; align-items: center; gap: 10px;
            }

            .status-dot {
                height: 10px; width: 10px; background-color: #00ffcc;
                border-radius: 50%; box-shadow: 0 0 10px #00ffcc;
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0% { opacity: 0.4; }
                70% { opacity: 1; }
                100% { opacity: 0.4; }
            }
        </style>
        
        <div class="custom-header">
            <div class="header-title">🚀 CRYPTOPORT <span style="font-size:12px; color:#94A3B8;">ELITE AI</span></div>
            <div class="user-badge">
                <span class="status-dot"></span>
                <span>SYSTEM ACTIVE</span> | 👤 """ + str(user_email) + """
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Sidebar Navigation with all features
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #00ffcc;'>MENU</h1>", unsafe_allow_html=True)
        
        # Define all features
        menu_options = {
            "📊 Dashboard": "dashboard",
            "📈 Trading Signals": "signals",
            "📉 Advanced Charts": "charts",
            "🔮 Forecast": "forecast",
            "⚠ Risk": "risk",
            "👤 Portfolio": "portfolio",
            "🤖 AI Assistant": "ai"
        }

        for label, key in menu_options.items():
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.session_state.page = label
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
