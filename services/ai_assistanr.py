from openai import OpenAI
from dotenv import load_dotenv
import os

# ============================================================
# LOAD ENV
# ============================================================

load_dotenv()

# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Crypto Investment Advisor.

Your responsibilities:
- Explain crypto simply
- Help beginners understand investing
- Explain RSI, trends, diversification
- Analyze portfolios
- Explain risk levels
- Give educational guidance only

Never guarantee profits.
Never give financial certainty.
Always keep responses beginner friendly.
"""

# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_ai(question, portfolio_data=None):

    context = ""

    if portfolio_data:

        context = f"""
        USER PORTFOLIO:
        {portfolio_data}
        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

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
        max_tokens=600
    )

    return response.choices[0].message.content
