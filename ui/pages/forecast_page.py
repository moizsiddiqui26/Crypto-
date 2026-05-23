import streamlit as st
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    st.markdown("# 🔮 AI Price Forecast")
    
    # NEW USER WELCOME
    st.info("💡 **New to Forecasting?** This tool uses Machine Learning to look at past price patterns and estimate where the price might go in 7 days. Remember: AI predictions are estimates, not guarantees!")

    coin = st.selectbox("Select Coin to Predict", sorted(df["Crypto"].unique()))
    amount = st.number_input("If I invest this much ($)...", value=1000.0, step=100.0)

    coin_df = df[df["Crypto"] == coin]
    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        st.markdown("### 📈 7-Day Prediction Results")
        col1, col2, col3 = st.columns(3)

        col1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        col2.metric("Expected Value", f"${result['expected_value']:.2f}")
        
        # Color coding the profit for beginners
        profit_val = result['profit_pct']
        col3.metric("Estimated Profit %", f"{profit_val:.2f}%", 
                    delta=f"{profit_val:.2f}%", delta_color="normal")

        # --- NEW USER EDUCATION SECTION ---
        with st.expander("📝 Understanding these numbers"):
            st.write(f"""
            - **Predicted Price:** This is what our AI thinks 1 {coin} will cost in 7 days.
            - **Expected Value:** If you invest ${amount:,.2f} today, this is what that total investment would be worth if the prediction comes true.
            - **Profit % (ROI):** 'Return on Investment.' A green number means the AI expects growth; a red number suggests a potential drop.
            """)
            
            st.warning("⚠️ **Risk Note:** Crypto is 'Volatile,' meaning prices move up and down very fast. Never invest money you cannot afford to lose.")
