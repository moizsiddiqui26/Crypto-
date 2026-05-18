from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are an advanced AI Crypto Investment Advisor.

Your job:
- Help beginners understand crypto.
- Explain risks.
- Suggest diversification.
- Analyze portfolio allocations.
- Explain RSI, MACD, trends.
- Give educational guidance only.

Never guarantee profits.
Always explain simply.
"""


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
                "content": f"{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.7,
        max_tokens=700
    )

    return response.choices[0].message.content
