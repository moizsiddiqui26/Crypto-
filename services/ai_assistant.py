import streamlit as st
import google.generativeai as genai

# ============================================================
# LOAD SECRET
# ============================================================

GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY"
)

# ============================================================
# CONFIGURE MODEL
# ============================================================

model = None

if GEMINI_API_KEY:

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(question, portfolio_data=None):

    if model is None:

        return """
❌ Gemini API key missing.

Go to:
Settings → Secrets

Add:

GEMINI_API_KEY = "your_key"
"""

    context = ""

    if portfolio_data:

        context = f"""
        USER PORTFOLIO:
        {portfolio_data}
        """

    prompt = f"""
    You are a crypto AI advisor.

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
