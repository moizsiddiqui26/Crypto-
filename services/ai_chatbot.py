import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# 🧠 CONTEXT BUILDER
# =========================
def build_context(portfolio_df=None, risk=None, forecast=None):

    context = "You are a crypto investment assistant.\n"

    if portfolio_df is not None:
        context += f"\nPortfolio:\n{portfolio_df.to_string()}\n"

    if risk is not None:
        context += f"\nRisk Level: {risk}\n"

    if forecast is not None:
        context += f"\nForecast Data: {forecast}\n"

    context += "\nGive short, clear investment insights."

    return context


# =========================
# 💬 CHAT FUNCTION
# =========================
def ask_ai(user_input, portfolio_df=None, risk=None, forecast=None):

    context = build_context(portfolio_df, risk, forecast)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast & cheap
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
