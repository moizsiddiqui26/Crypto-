import streamlit as st
import time

def render_chatbot():
    st.markdown('<div class="section-title">🤖 AI Crypto Assistant</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** Ask me anything! For example: 'Should I buy Bitcoin right now?' or 'Can you explain what a market cycle is?' I use advanced AI to analyze sentiment and simplify crypto data for you.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! I'm your AI Crypto Advisor. How can I help you invest safely today?"}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question (e.g., Should I buy Solana?)..."):
        # User message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response mapping (Mocked ML Pipeline)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing market sentiment and ML indicators..."):
                time.sleep(1.5)
                
                response = "I couldn't analyze that specific query."
                p_lower = prompt.lower()
                if "solana" in p_lower or "sol" in p_lower:
                    response = "**Solana (SOL)** currently shows bullish momentum with increasing volume and positive sentiment. Risk level is medium. Consider a gradual 'Dollar-Cost Averaging' plan instead of investing all at once."
                elif "bitcoin" in p_lower or "btc" in p_lower:
                    response = "**Bitcoin (BTC)** is currently facing support levels at historical moving averages. The AI model predicts a 70% confidence of upward momentum over the next week. A great time to hold or accumulate."
                elif "what is" in p_lower:
                    response = "Let's simplify that! In crypto, terms can be confusing. Basically, that means tracking the overall 'mood' or logic of the market to see if people are aggressively buying or safely holding."
                else:
                    response = "Based on my real-time Machine Learning models, the broader market is currently in a slightly bullish accumulation phase. Keep investments distributed and track your risk."
                
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.markdown('</div>', unsafe_allow_html=True)
