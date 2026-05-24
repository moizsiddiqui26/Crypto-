import streamlit as st
import pandas as pd
from services.ai_assistant import ask_ai
from db.models import get_holdings

def render_chatbot_page(df):
    st.markdown("# 🤖 AI Investment Assistant")

    # ============================================================
    # NEW USER GUIDE (Beginner Friendly)
    # ============================================================
    with st.expander("📖 New User Guide: How to use this AI"):
        st.markdown("""
        ### Welcome to your AI Copilot! 
        You don't need to be a professional trader to get value here. Think of this AI as your **financial mentor**.
        
        **Things you can ask:**
        - **"Explain Bitcoin like I'm 5"** — Great for understanding the basics.
        - **"Is it a good time to buy Ethereum?"** — AI analyzes the current charts and trends for you.
        - **"How can I lower my portfolio risk?"** — AI looks at your current holdings and suggests safer moves.
        """)
        st.info("💡 **Pro Tip:** Be specific. Instead of asking 'Is BTC good?', try 'Is BTC a good long-term hold given its current volatility?'")

    st.markdown("---")

    # ============================================================
    # AI COMMAND CENTER
    # ============================================================
    col_chat, col_tools = st.columns([3, 1])

    # Portfolio Context for AI
    email = st.session_state.get("email")
    holdings = get_holdings(email)
    portfolio_summary = ""
    if holdings:
        pf = pd.DataFrame(holdings, columns=["Crypto", "Amount", "Date"])
        portfolio_summary = pf.to_string()

    with col_tools:
        st.markdown("### ⚡ Quick Actions")
        # Buttons that pre-fill the AI query
        if st.button("📈 Analyze Trends", use_container_width=True):
            st.session_state.temp_prompt = "Analyze the top 3 coins based on recent trends."
        if st.button("🛡️ Check My Risk", use_container_width=True):
            st.session_state.temp_prompt = "Based on my portfolio data, is my risk level too high?"
        if st.button("🔮 7-Day Forecast", use_container_width=True):
            st.session_state.temp_prompt = "Give me a 7-day price forecast for the main coins."

    with col_chat:
        st.markdown("### 💬 Chat with AI")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display history
        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(msg)

        # Chat Input logic handling both manual text and Quick Action buttons
        user_input = st.chat_input("Ask your AI crypto advisor...")
        
        # If a Quick Action button was clicked, it overrides user_input
        active_prompt = st.session_state.get('temp_prompt') or user_input

        if active_prompt:
            # Clear button state after use
            if 'temp_prompt' in st.session_state:
                st.session_state.temp_prompt = None

            st.session_state.chat_history.append(("user", active_prompt))
            with st.chat_message("user"):
                st.markdown(active_prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing market data..."):
                    response = ask_ai(active_prompt, portfolio_summary)
                    st.markdown(response)
            
            st.session_state.chat_history.append(("assistant", response))

    # ============================================================
    # BEGINNER'S DICTIONARY
    # ============================================================
    st.markdown("---")
    st.subheader("📚 Beginner's Crypto Dictionary")
    d1, d2, d3 = st.columns(3)
    
    with d1:
        st.markdown("**🚀 Bull Market**")
        st.caption("When prices are going up consistently. Everyone is optimistic!")
    
    with d2:
        st.markdown("**🐻 Bear Market**")
        st.caption("When prices are falling and the market is 'hibernating'.")
    
    with d3:
        st.markdown("**💎 HODL**")
        st.caption("A term for holding your assets long-term, no matter what happens.")
