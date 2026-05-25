import streamlit as st
import pandas as pd
import os
import sys

# --- PATH FIX FOR ROBUST IMPORTS ---
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from services.ai_assistant import ask_ai
    from db.models import get_holdings
except ImportError:
    st.error("Error loading backend services.")

def render_chatbot_page(df):
    # Professional Header with Status Indicator
    h_col1, h_col2 = st.columns([4, 1])
    with h_col1:
        st.markdown('<div class="section-title">🤖 AI Investment Copilot</div>', unsafe_allow_html=True)
    with h_col2:
        st.markdown('<p style="color:#00ffcc; text-align:right; font-size:12px;">● System Online</p>', unsafe_allow_html=True)

    # ============================================================
    # 📘 ENHANCED USER GUIDE & QUICK ACTIONS
    # ============================================================
    with st.expander("📖 AI Mastery Guide: Get better results", expanded=False):
        st.markdown("""
        **How to talk to your Copilot:**
        1. **Portfolio Reviews**: Ask *"Should I rebalance my current holdings?"*
        2. **Technical Education**: Ask *"What is the difference between Proof of Work and Proof of Stake?"*
        3. **Market Sentiment**: Ask *"What is the market sentiment for Ethereum today?"*
        """)
        st.info("💡 **Pro Tip:** The AI has access to your current portfolio data and live market prices.")

    st.markdown("---")

    # ============================================================
    # 🛠️ SIDEBAR-STYLE TOOLS (PORTFOLIO CONTEXT)
    # ============================================================
    col_chat, col_tools = st.columns([2.5, 1])

    # Portfolio Context for AI
    email = st.session_state.get("email")
    holdings = get_holdings(email)
    portfolio_summary = "User has no holdings."
    
    with col_tools:
        st.markdown("### 🧳 Your Context")
        if holdings:
            pf = pd.DataFrame(holdings, columns=["Crypto", "Amount", "Date"])
            portfolio_summary = pf.to_string()
            st.success(f"✅ AI synced with {len(pf)} assets")
            st.caption("AI is currently analyzing your holdings to provide personalized advice.")
        else:
            st.warning("⚠️ No holdings found. AI will provide general market advice.")
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        # Quick Action Buttons that trigger chat
        if st.button("📊 Review Portfolio", use_container_width=True):
            st.session_state.temp_prompt = "Based on my current holdings, what is my risk level?"
        if st.button("📈 Trend Forecast", use_container_width=True):
            st.session_state.temp_prompt = "Which top 3 coins show the best trend for next week?"
        if st.button("📉 Risk Check", use_container_width=True):
            st.session_state.temp_prompt = "Explain the current market RSI and if it's safe to buy."

    # ============================================================
    # 💬 PREMIUM CHAT INTERFACE
    # ============================================================
    with col_chat:
        # Chat container for scrollable area
        chat_container = st.container(height=500, border=True)
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                ("assistant", "Hello! I am your AI Investment Copilot. I have access to your portfolio and live market data. How can I help you today?")
            ]

        # Display history within the container
        with chat_container:
            for role, msg in st.session_state.chat_history:
                with st.chat_message(role):
                    st.markdown(msg)

        # Input handling
        user_input = st.chat_input("Message your Copilot...")
        
        # Override user_input if a Quick Action was clicked
        active_prompt = st.session_state.get('temp_prompt') or user_input

        if active_prompt:
            # Clear button state after use
            if 'temp_prompt' in st.session_state:
                st.session_state.temp_prompt = None

            # Add user message
            st.session_state.chat_history.append(("user", active_prompt))
            
            # This triggers a rerun to show the user message immediately, 
            # then the assistant will process on the next loop.
            with st.chat_message("user"):
                st.markdown(active_prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    response = ask_ai(active_prompt, portfolio_summary)
                    st.markdown(response)
                    st.session_state.chat_history.append(("assistant", response))
            
            st.rerun()

    # ============================================================
    # 📚 DESIGNER DICTIONARY (STYLIZED)
    # ============================================================
    st.markdown("---")
    st.markdown("### 🏛️ Crypto Knowledge Hub")
    
    # CSS for nice cards
    st.markdown("""
        <style>
        .crypto-card {
            background-color: #1a1a3a;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #00ffcc;
            height: 120px;
        }
        </style>
    """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown('<div class="crypto-card"><b>🚀 Bull Market</b><br><small>Consistent price increases. High optimism and buying pressure.</small></div>', unsafe_allow_html=True)
    with d2:
        st.markdown('<div class="crypto-card"><b>🐻 Bear Market</b><br><small>Sustained price drops. Market "hibernation" and caution.</small></div>', unsafe_allow_html=True)
    with d3:
        st.markdown('<div class="crypto-card"><b>💎 HODL</b><br><small>A long-term strategy of holding assets regardless of volatility.</small></div>', unsafe_allow_html=True)
