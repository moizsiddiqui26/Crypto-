import os
import pandas as pd
from openai import OpenAI

# =========================
# 🔐 INIT CLIENT
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# 🧠 BUILD CONTEXT
# =========================
def build_context(portfolio_df=None, risk=None, forecast=None):
    context = "You are a crypto investment assistant.\n"

    # Portfolio
    if portfolio_df is not None and not portfolio_df.empty:
        context += "\nUser Portfolio:\n"
        context += portfolio_df.to_string(index=False)
        context += "\n"

    # Risk
    if risk is not None:
        context += f"\nPortfolio Risk Level: {risk}\n"

    # Forecast
    if forecast is not None:
        context += "\nForecast Summary:\n"
        context += f"Predicted Price: {forecast.get('predicted_price', 'N/A')}\n"
        context += f"Expected Value: {forecast.get('expected_value', 'N/A')}\n"
        context += f"Profit %: {forecast.get('profit_pct', 'N/A')}\n"

    context += "\nGive short, clear, practical investment advice."

    return context


# =========================
# 💬 ASK AI
# =========================
def ask_ai(user_input, portfolio_df=None, risk=None, forecast=None):

    try:
        context = build_context(portfolio_df, risk, forecast)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠ AI Error: {str(e)}"
