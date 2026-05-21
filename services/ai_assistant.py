import google.generativeai as genai
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    try:
        # Get API Key from secrets or environment
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ AI Error: Google API Key not found in Streamlit Secrets."

        genai.configure(api_key=api_key)

        # FIX: Use 'gemini-1.5-flash' instead of 'gemini-1.5-flash-latest' 
        # to ensure compatibility with v1 and v1beta endpoints.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Construct a professional prompt including user portfolio data
        prompt = f"""
        You are a professional Crypto Investment AI Advisor. 
        
        USER PORTFOLIO DATA:
        {portfolio_context if portfolio_context else "No active holdings yet."}

        USER QUESTION:
        {user_query}

        Instructions:
        1. Give concise, data-driven advice.
        2. Always include a disclaimer that you are an AI, not a financial advisor.
        3. If the user asks about their specific holdings, refer to the data provided above.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # Better error reporting to help you debug
        error_msg = str(e)
        if "404" in error_msg:
            return "❌ AI Error: The selected Gemini model is currently unavailable. Please try 'gemini-1.5-flash' or check your region settings."
        return f"⚠️ AI Assistant is currently offline. Error: {error_msg}"
