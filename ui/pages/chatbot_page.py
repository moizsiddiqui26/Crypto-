import streamlit as st

# ==========================================================
# SAFE IMPORTS
# ==========================================================
try:
    from services.ai_assistant import ask_ai
except Exception as e:
    st.error(f"AI Assistant Import Error: {e}")
    st.stop()

try:
    from db.models import get_holdings
except Exception as e:
    st.error(f"Database Import Error: {e}")
    st.stop()


def render_chatbot_page(df):
    st.title("🤖 AI Crypto Assistant")

    email = st.session_state.get("email", "")

    # ==========================================================
    # GET USER HOLDINGS SAFELY
    # ==========================================================
    try:
        holdings = get_holdings(email)
    except Exception as e:
        st.error(f"Unable to fetch portfolio holdings: {e}")
        holdings = []

    st.subheader("Your Portfolio")

    if holdings:
        for crypto, amount, date in holdings:
            st.write(f"• {crypto}: {amount}")
    else:
        st.info("No holdings found.")

    user_query = st.text_input(
        "Ask me anything about crypto, your portfolio, or market trends:"
    )

    if st.button("Ask AI"):
        if user_query:

            try:
                response = ask_ai(
                    question=user_query,
                    portfolio=holdings,
                    market_data=df
                )

                st.success(response)

            except Exception as e:
                st.error(f"AI Error: {e}")
