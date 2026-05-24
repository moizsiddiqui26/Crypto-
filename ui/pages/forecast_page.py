import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    # --- 1. SELECTION SECTION ---
    st.markdown("# 🔮 AI Price Intelligence")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        st.markdown("### Select Asset to Analyze")
        coin = st.selectbox("", sorted(df["Crypto"].unique()), label_visibility="collapsed")
    with col_sel2:
        st.markdown("### Hypothetical Investment ($)")
        amount = st.number_input("", value=1000.0, label_visibility="collapsed")

    # --- 2. FUTURE FORECAST RESULTS ---
    st.markdown("---")
    st.markdown("### 🚀 Future Forecast (Next 7 Days)")
    
    # Process data for the specific coin
    # Grouping by Date ensures we have one unique price per day
    coin_df = df[df["Crypto"] == coin].copy()
    coin_df['Date'] = pd.to_datetime(coin_df['Date']).dt.normalize()
    coin_df = coin_df.groupby('Date')['Close'].mean().reset_index().sort_values("Date")
    
    if len(coin_df) < 14:
        st.warning("⚠️ Insufficient historical data for this asset.")
        return

    # Call the engine for future prediction
    result = get_forecast_summary(coin_df, amount, 7)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Target Price", f"${result['predicted_price']:.2f}")
    f2.metric("Portfolio Goal", f"${result['expected_value']:.2f}")
    f3.metric("Growth Potential", f"{result['profit_pct']:.2f}%", delta=f"{result['profit_pct']:.2f}%")

    # --- 3. NEW USER TIPS (Beginner's Explanation) ---
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

    # --- 4. AI PERFORMANCE REVIEW (Backtesting Last 7 Days) ---
    st.markdown("---")
    st.markdown("### 🏆 AI Performance Review (Last 7 Working Days)")
    
    # Backtesting Logic: Hide the last 7 days and predict them
    train_data = coin_df.iloc[:-7].reset_index(drop=True)
    actual_last_7 = coin_df.iloc[-7:].reset_index(drop=True)
    
    # Train model on past data
    X_train = np.arange(len(train_data)).reshape(-1, 1)
    y_train = train_data["Close"]
    model = LinearRegression().fit(X_train, y_train)
    
    # Predict the 7 days that already happened
    X_test = np.arange(len(train_data), len(train_data) + 7).reshape(-1, 1)
    predicted_last_7 = model.predict(X_test)

    # Create Table with Correct Unique Dates
    comparison_df = pd.DataFrame({
        "Date": actual_last_7["Date"].dt.strftime('%Y-%m-%d'),
        "Actual Price": actual_last_7["Close"].values,
        "AI Prediction": predicted_last_7,
    })
    
    comparison_df["Difference (%)"] = ((comparison_df["AI Prediction"] - comparison_df["Actual Price"]) / comparison_df["Actual Price"]) * 100
    
    # Styling for the table
    def style_diff(val):
        color = '#ff4b4b' if abs(val) > 5 else '#00ffcc'
        return f'color: {color}; font-weight: bold;'

    styled_table = comparison_df.style.format({
        "Actual Price": "${:,.2f}",
        "AI Prediction": "${:,.2f}",
        "Difference (%)": "{:,.2f}%"
    }).map(style_diff, subset=['Difference (%)'])

    st.table(styled_table)

    # Accuracy Summary Metrics
    avg_err = comparison_df["Difference (%)"].abs().mean()
    m1, m2 = st.columns(2)
    m1.write(f"**Average Model Deviation:** {avg_err:.2f}%")
    m2.write("**Model Reliability:** ✅ High" if avg_err < 10 else "⚠️ Moderate")
