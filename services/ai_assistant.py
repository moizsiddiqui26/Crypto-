from openai import OpenAI
import streamlit as st

# ============================================================
# LOAD API KEY
# ============================================================

OPENAI_API_KEY = st.secrets["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"]

# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a professional AI Crypto Investment Advisor.

You help beginners understand:
- cryptocurrency
- portfolio diversification
- trading signals
- RSI and indicators
- risk management
- market trends

Always explain simply.
Never guarantee profits.
"""

# ============================================================
# ASK AI
# ============================================================

def ask_ai(question, portfolio_data=None):

    context = ""

    if portfolio_data:

        context = f"""
        USER PORTFOLIO:
        {portfolio_data}
        """

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": f"{context}\n\nQUESTION:\n{question}"
                }

            ],

            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Error: {str(e)}"
