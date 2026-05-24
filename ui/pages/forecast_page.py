import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    # --- 1. PRO UI HEADER ---
    st.markdown("# 🔮 AI Price Intelligence & Backtesting")
    
    st.markdown("""
        <div style="background: rgba(0, 255, 204, 0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; margin-bottom: 25px;">
            <p style="margin:0; color: #00ffcc; font-weight: 600;">
                💡 NEW USER TIP: Professional traders don't look for 100% accuracy; they look for "Directional Fit." 
                If the AI's trend matches the market direction, the model is working.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Asset Selection
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        coin = st.selectbox("Select Asset to Analyze", sorted(df["Crypto"].unique()))
    with col_sel2:
        amount = st.number_input("Hypothetical Investment ($):", value=1000.0)

    # Filter data for selected coin
    coin_df = df[df["Crypto"] == coin].sort_values("Date").reset_index(drop=True)
    
    if len(coin_df) < 14:
        st.warning("Not enough historical data to perform backtesting.")
        return

    # --- 2. THE BACKTESTING LOGIC (Last 7 Days) ---
    # We "hide" the last 7 days from the model to see what it would have predicted
    train_data = coin_df.iloc[:-7]
    actual_last_7 = coin_df.iloc[-7:]
    
    # Train model on historical data only
    t_train = np.arange(len(train_data)).reshape(-1, 1)
    y_train = train_data["Close"]
    model = LinearRegression().fit(t_train, y_train)
    
    # Predict the last 7 days (The "Guess")
    t_test = np.arange(len(train_data), len(train_data) + 7).reshape(-1, 1)
    predicted_last_7 = model.predict(t_test)

    # --- 3. DISPLAY PERFORMANCE SCORECARD ---
    st.markdown("### 🏆 AI Performance (Last 7 Days vs. Actual)")
    
    # Create Comparison Table
    comparison_df = pd.DataFrame({
        "Date": actual_last_7["Date"].dt.strftime('%Y-%m-%d'),
        "Actual Price": actual_last_7["Close"].values,
        "AI Prediction": predicted_last_7,
    })
    
    # Calculate Error %
    comparison_df["Difference (%)"] = ((comparison_df["AI Prediction"] - comparison_df["Actual Price"]) / comparison_df["Actual Price"]) * 100
    
    # UI Styling for Table
    def color_delta(val):
        color = '#ff4b4b' if abs(val) > 5 else '#00ffcc'
        return f'color: {color}'

    st.table(comparison_df.style.format({
        "Actual Price": "${:,.2f}",
        "AI Prediction": "${:,.2f}",
        "Difference (%)": "{:,.2f}%"
    }).applymap(color_delta, subset=['Difference (%)']))

    # --- 4. ACCURACY METRICS ---
    st.markdown("---")
    avg_error = comparison_df["Difference (%)"].abs().mean()
    r2 = r2_score(actual_last_7["Close"], predicted_last_7)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg. Model Error", f"{avg_error:.2f}%")
    c2.metric("Trend Confidence (R²)", f"{max(0, r2*100):.1f}%")
    
    direction_correct = 0
    # Simple logic to check if both predicted an increase or both a decrease
    for i in range(1, len(comparison_df)):
        act_up = actual_last_7["Close"].iloc[i] > actual_last_7["Close"].iloc[i-1]
        pred_up = predicted_last_7[i] > predicted_last_7[i-1]
        if act_up == pred_up: direction_correct += 1
    
    c3.metric("Directional Accuracy", f"{int((direction_correct/6)*100)}%")

    # --- 5. FUTURE PREDICTION ---
    st.markdown("---")
    st.markdown("### 🔮 Future 7-Day Outlook")
    
    # Now get the actual forecast using ALL current data
    result = get_forecast_summary(coin_df, amount, 7)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Target Price", f"${result['predicted_price']:.2f}")
    f2.metric("Expected Portfolio", f"${result['expected_value']:.2f}")
    f3.metric("Growth Potential", f"{result['profit_pct']:.2f}%", delta=f"{result['profit_pct']:.2f}%")

    with st.expander("📝 Guide: How to Read this Report"):
        st.write("""
        1. **Actual vs Prediction:** If the 'Difference' column is small and green, the market is currently following a linear trend.
        2. **Directional Accuracy:** This is the most important metric. It shows how often the AI correctly guessed if the price would move UP or DOWN.
        3. **Confidence (R²):** High percentage means the asset is stable. Low percentage means the asset is too volatile for linear models.
        """)
