from groq import Groq
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    try:
        # 1. Fetch the Groq API Key
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            return "⚠️ Setup Required: Please add 'GROQ_API_KEY' to your Streamlit secrets."

        # 2. Initialize the Groq Client
        client = Groq(api_key=api_key)
        
        # 3. Generate completion using Llama 3
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional Crypto Advisor assistant for 'CryptoPort AI'. "
                        "Provide concise, data-driven advice. "
                        f"Context: {portfolio_context}"
                    )
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        return f"⚠️ Groq Assistant Error: {str(e)}"
