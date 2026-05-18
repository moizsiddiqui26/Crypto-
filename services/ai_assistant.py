import google.generativeai as genai
import streamlit as st

# ============================================================
# CONFIGURE GEMINI
# ============================================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(question, portfolio_data=None):

    context = ""

    if portfolio_data:

        context = f"""
        USER PORTFOLIO:
        {portfolio_data}
        """

    prompt = f"""
    You are an AI Crypto Investment Advisor.

    Help beginners understand:
    - cryptocurrency
    - diversification
    - portfolio risk
    - RSI
    - trading signals

    Never guarantee profits.

    {context}

    USER QUESTION:
    {question}
    """

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"
