import google.generativeai as genai
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    """
    Connects to Google Gemini AI to provide crypto investment advice.
    """
    try:
        # 1. RETRIEVE API KEY
        # Ensure 'GOOGLE_API_KEY' is added to your .streamlit/secrets.toml
        api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            return "⚠️ AI Error: Google API Key not found. Please add 'GOOGLE_API_KEY' to your Streamlit Secrets."

        # 2. CONFIGURE GENERATIVE AI
        genai.configure(api_key=api_key)

        # 3. INITIALIZE MODEL
        # We use 'gemini-1.5-flash' which is the stable production name.
        # Avoid using '-latest' if your library version is older.
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 4. CONSTRUCT THE PROMPT
        # We provide the AI with your portfolio data for personalized answers.
        prompt = f"""
        You are a professional Crypto Investment AI Advisor named 'Gemini Crypto Copilot'.
        
        CONTEXT (User's Current Portfolio):
        {portfolio_context if portfolio_context else "The user currently has no recorded holdings."}

        USER QUESTION:
        {user_query}

        INSTRUCTIONS:
        - Provide data-driven, concise, and helpful advice.
        - If the user asks about their specific coins (BTC, BNB, etc.), refer to the Context provided.
        - Always end with a short disclaimer: 'Note: I am an AI, not a financial advisor.'
        """

        # 5. GENERATE RESPONSE
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "⚠️ AI Error: The model returned an empty response. Please try rephrasing your question."

    except Exception as e:
        error_msg = str(e)
        # Specific troubleshooting for common errors
        if "404" in error_msg:
            return "❌ AI Error: Model 'gemini-1.5-flash' not found. Ensure your google-generativeai library is updated."
        elif "API_KEY_INVALID" in error_msg:
            return "❌ AI Error: Your Google API Key is invalid. Please check it in AI Studio."
        else:
            return f"⚠️ AI Assistant Error: {error_msg}"
