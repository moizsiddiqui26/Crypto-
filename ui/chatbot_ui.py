import streamlit as st
import time
from ai_assistant import ask_ai  # Import the new Groq logic

def render_chatbot():
    st.markdown('<div class="section-title">🤖 AI Crypto Assistant (Groq Powered)</div>', unsafe_allow_html=True)
    st.info("💡 **Speed Update:** Now powered by Groq Llama 3 for real-time market analysis.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! I'm your AI Crypto Advisor. How can I help you invest safely today?"}
        ]

    # Display History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle Input
    if prompt := st.chat_input("Ask about Bitcoin, Solana, or market trends..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Groq is analyzing..."):
                # Call the real AI engine
                response = ask_ai(prompt)
                
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.markdown('</div>', unsafe_allow_html=True)
