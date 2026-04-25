import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(user_input, context_data=None):

    system_prompt = f"""
    You are CRYPTOPORT AI — a professional crypto investment assistant.

    Provide:
    - Clear insights
    - Buy/Sell suggestions
    - Risk warnings

    Market Data:
    {context_data}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠ AI Error: {str(e)}"
