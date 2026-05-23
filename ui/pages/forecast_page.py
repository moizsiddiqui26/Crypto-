import streamlit as st
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    st.markdown("# 🔮 AI Price Forecast")
    
    # ---------------------------------------------------------
    # NEW USER WELCOME & GUIDE
    # ---------------------------------------------------------
    st.markdown("""
        <div style="background-color: #171924; padding: 20px; border-radius: 10px; border-left: 5px solid #3861FB; margin-bottom: 25px;">
            <h4 style="margin-top:0;">🌟 New to AI Forecasting?</h4>
            <p style="color: #A1A7BB; font-size: 14px;">
                Our Machine Learning models analyze years of price data to spot patterns. 
                Below, you can select a coin and an investment amount to see a <b>7-Day Prediction</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # User Inputs
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        coin = st.selectbox("Which crypto should we analyze?", sorted(df["Crypto"].unique()))
    with col_input2:
        amount = st.number_input("If you invested this amount ($):", value=1000.0, step=100.0)

    # ---------------------------------------------------------
    # FORECAST CALCULATION
    # ---------------------------------------------------------
    coin_df = df[df["Crypto"] == coin]
    # We use a 7-day window for the forecast
    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        st.markdown("---")
        st.subheader(f"📈 7-Day Forecast for {coin}")
        
        # Displaying Results in Metric Cards
        m1, m2, m3 = st.columns(3)
        
        # Predicted Price
        m1.metric(
            label="Predicted Price", 
            value=f"${result['predicted_price']:.2f}",
            help="The price our AI expects in 1 week."
        )
        
        # Expected Total Value
        m2.metric(
            label="Value in 7 Days", 
            value=f"${result['expected_value']:.2f}",
            help="What your total investment would be worth."
        )
        
        # Profit Percentage (ROI)
        profit_pct = result['profit_pct']
        m3.metric(
            label="Estimated Growth", 
            value=f"{profit_pct:.2f}%",
            delta=f"{profit_pct:.2f}%",
            help="ROI (Return on Investment) - Green means profit, Red means loss."
        )

        # ---------------------------------------------------------
        # THE BEGINNER'S DICTIONARY
        # ---------------------------------------------------------
        st.markdown("### 📝 What do these numbers mean?")
        
        with st.expander("🔍 Click here to see the Beginner's Explanation"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**What is ROI?**")
                st.write("""
                ROI stands for **Return on Investment**. 
                - If it's **+5%**, your $1,000 becomes $1,050.
                - If it's **-5%**, your $1,000 becomes $950.
                """)
            with col_b:
                st.write("**How accurate is this?**")
                st.write("""
                Predictions are based on **Historical Trends**. If the market changes suddenly due to news or global events, the AI may not be 100% accurate. 
                """)

            st.info("💡 **Pro Tip:** Don't put all your money in one coin. Use the 'Risk' page to see which coins are the safest!")

    else:
        st.error("Not enough data to generate a forecast for this coin. Try selecting a different asset.")

    # ---------------------------------------------------------
    # VISUAL AID FOR BEGINNERS
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📊 How the AI 'Thinks'")
    
    st.caption("The AI looks at the blue 'Past' line to project the dotted 'Future' line.")
