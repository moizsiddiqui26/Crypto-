import streamlit as st
import pandas as pd

from services.ai_assistant import ask_ai
from db.models import get_holdings


def render_chatbot_page(df):

    st.markdown("# 🤖 Gemini Crypto Copilot")

    st.info(
        """
        Ask anything about:
        - Bitcoin
        - Ethereum
        - RSI
        - Trading
        - Portfolio Risk
        - Diversification
        """
    )

    email = st.session_state.get("email")

    holdings = get_holdings(email)

    portfolio_summary = ""

    if holdings:

        pf = pd.DataFrame(
            holdings,
            columns=["Crypto", "Amount", "Date"]
        )

        portfolio_summary = pf.to_string()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:

        with st.chat_message(role):
            st.markdown(msg)

    user_input = st.chat_input(
        "Ask your AI crypto advisor..."
    )

    if user_input:

        st.session_state.chat_history.append(
            ("user", user_input)
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner("Gemini AI analyzing market trends..."):

                response = ask_ai(
                    user_input,
                    portfolio_summary
                )

                st.markdown(response)

        st.session_state.chat_history.append(
            ("assistant", response)
        )
