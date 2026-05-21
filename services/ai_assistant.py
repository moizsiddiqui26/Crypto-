import google.generativeai as genai
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ Setup Required: Please add a new API Key to your secrets."

        genai.configure(api_key=api_key)
        # Use the 2026 standard model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(f"Context: {portfolio_context}\n\nUser: {user_query}")
        return response.text

    except Exception as e:
        error_str = str(e)
        
        # Handle the 403 "Project Denied" Error specifically
        if "403" in error_str:
            # Check for common crypto questions to provide local answers
            q = user_query.lower()
            if "bitcoin" in q or "btc" in q:
                return "📢 **(Advisor in Safe Mode):** Bitcoin is a decentralized digital asset. Currently, your API project is restricted (403). Please create a new Project in AI Studio to restore full AI features."
            
            return "❌ **AI Project Blocked (403):** Google has restricted this project due to a previous security leak. To fix this, please create a *new* project in AI Studio and update your API key."
            
        return f"⚠️ Assistant Error: {error_str}"
