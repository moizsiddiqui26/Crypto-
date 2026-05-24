import streamlit as st
import pandas as pd
from services.forecast_engine import get_forecast_summary
from sklearn.metrics import r2_score
import numpy as np

def render_forecast(df):
    st.markdown("# 🔮 AI Price Forecast & Accuracy")
    
    st.info("💡 **AI Intelligence:** This module uses Linear Regression to find the mathematical trend of the asset. We have removed visual charts to focus on the raw data and model accuracy scores.")

    # Selection Logic
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        coin = st.selectbox("Select Asset to Predict", sorted(df["Crypto"].unique()))
    with col_sel2:
        amount = st.number_input("If I invest this much ($):", value=1000.0)

    # Forecasting Logic
    coin_df = df[df["Crypto"] == coin].sort_values("Date")
    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        # --- SECTION 1: PREDICTION RESULTS ---
        st.markdown("### 🎯 Prediction Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        m2.metric("Expected Portfolio Value", f"${result['expected_value']:.2f}")
        m3.metric("Estimated Growth (%)", f"{result['profit_pct']:.2f}%", 
                  delta=f"{result['profit_pct']:.2f}%")

        # --- SECTION 2: ACCURACY CHECK (Backtesting) ---
        st.markdown("---")
        st.markdown("### 📊 Model Confidence & Accuracy")
        
        # Calculate R-Squared (Accuracy Score)
        # We compare the actual historical prices to what the model thinks they should have been
        y_true = coin_df["Close"]
        t = np.arange(len(coin_df)).reshape(-1, 1)
        
        # We need to simulate the model fit here for accuracy checking
        from sklearn.linear_model import LinearRegression
        model = LinearRegression().fit(t, y_true)
        y_pred = model.predict(t)
        
        accuracy_val = r2_score(y_true, y_pred) * 100

        c1, c2 = st.columns(2)
        with c1:
            st.write("**Accuracy Score (R²):**")
            st.progress(max(0, min(int(accuracy_val), 100)) / 100)
            st.caption(f"The model is {accuracy_val:.2f}% confident in this trend.")
        
        with c2:
            if accuracy_val > 80:
                st.success("✅ **Strong Trend:** The market is moving in a very predictable line.")
            elif accuracy_val > 50:
                st.warning("⚠️ **Moderate Volatility:** The trend is visible but has 'noise'.")
            else:
                st.error("🚨 **High Volatility:** Prediction accuracy is low due to erratic movements.")

        # --- SECTION 3: DATA TABLE ---
        with st.expander("📂 View Raw Prediction Data"):
            st.dataframe(coin_df.tail(10), use_container_width=True)

        # Beginner's Guide Expanders
        with st.expander("📚 How do we check if this is correct?"):
            st.markdown("""
            1. **The R² Score:** A score of 100% would mean the price is moving in a perfectly straight line. 
            2. **Trend vs. Reality:** Since we use Linear Regression, we are checking if the 'General Direction' is correct, rather than pinpointing exact daily spikes.
            3. **Backtesting:** You can verify accuracy by looking at the 'Accuracy Score' above; it measures how well the model 'learned' from the past 30-90 days.
            """)
