import streamlit as st
import google.generativeai as genai

# ============================================================
# LOAD SECRET
# ============================================================

GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY"
)

# ============================================================
# CONFIGURE GEMINI
# ============================================================

model = None

if GEMINI_API_KEY:

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    model = genai.GenerativeModel(
        "gemini-1.5-flash-latest"
    )

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Crypto Investment Advisor.

Help users understand:
- cryptocurrency
- Bitcoin
- Ethereum
- diversification
- RSI
- risk management
- trading basics

Never guarantee profits.
Keep responses beginner friendly.
"""

# ============================================================
# ASK AI
# ============================================================

def ask_ai(question, portfolio_data=None):

    if model is None:

        return """
❌ Gemini API key missing.

Add GEMINI_API_KEY inside Streamlit Secrets.
"""

    context = ""

    if portfolio_data:

        context = f"""
        USER PORTFOLIO:
        {portfolio_data}
        """

    prompt = f"""
    {SYSTEM_PROMPT}

    {context}

    USER QUESTION:
    {question}
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"AI Error: {str(e)}"
