import google.generativeai as genai
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    """
    Crypto Advisor with Fallback Mode for 403/Region errors.
    """
    # --- 1. LOCAL FALLBACK KNOWLEDGE (For when API is blocked) ---
    local_kb = {
        "bitcoin": "Bitcoin (BTC) is a decentralized digital currency, often called 'Digital Gold'. It works on a public ledger called Blockchain.",
        "bnb": "BNB is the native coin of the Binance ecosystem, used for trading fee discounts and powering the BNB Smart Chain.",
        "rsi": "RSI (Relative Strength Index) is a momentum indicator that measures if a coin is 'Overbought' (above 70) or 'Oversold' (below 30).",
        "portfolio": f"Based on your data: {portfolio_context[:100]}..."
    }

    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ Please add your GOOGLE_API_KEY to secrets."

        genai.configure(api_key=api_key)
        
        # Try the most stable model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"User Portfolio: {portfolio_context}\n\nQuestion: {user_query}\n\nKeep it short."
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_msg = str(e)
        
        # --- 2. HANDLE 403 DENIED ACCESS ---
        if "403" in error_msg:
            # Look for a keyword in the user query to provide a local answer
            query_lower = user_query.lower()
            for key in local_kb:
                if key in query_lower:
                    return f"📢 **(Local Assistant Mode):** {local_kb[key]}\n\n*Note: Your API is currently blocked (403), using offline knowledge.*"
            
            return "❌ **AI Access Denied (403).** This is usually a regional restriction by Google. Please check your AI Studio settings or use a different network/VPN."
        
        return f"⚠️ Error: {error_msg}"
