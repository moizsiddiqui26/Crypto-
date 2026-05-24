import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    # --- 1. PRO UI HEADER (FULL WIDTH) ---
    st.markdown("# 🔮 AI Price Intelligence & Backtesting")
    
    # NEW USER TIP: Professional Branding
    st.markdown("""
        <div style="background: rgba(0, 255, 204, 0.05); padding: 20px; border-radius: 12px; border-left: 5px solid #00ffcc; margin-bottom: 30px;">
            <h4 style="margin:0; color: #00ffcc;">💡 Intelligence Tip for New Users</h4>
            <p style="margin:5px 0 0 0; color: #94A3B8; font-size: 14px;">
                <b>Don't chase exact prices.</b> Financial AI is built to identify <b>Trend Velocity</b>. 
                If the 'Directional Accuracy' is above 70%, the model is successfully capturing the market's momentum, 
                even if the exact dollar amount varies due to daily volatility.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Asset Selection
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        coin = st.selectbox("Select Asset to Analyze", sorted(df["Crypto"].unique()))
    with col_sel2:
        amount = st.number_input("Hypothetical Investment ($):", value=1000.0)

    # Data Preparation
    coin_df = df[df["Crypto"] == coin].sort_values("Date").reset_index(drop=True)
    
    if len(coin_df) < 14:
        st.warning("⚠️ Insufficient data for backtesting. Need at least 14 days of history.")
        return

    # --- 2. THE BACKTESTING LOGIC (Simulating the Last 7 Days) ---
    train_data = coin_df.iloc[:-7]
    actual_last_7 = coin_df.iloc[-7:].copy()
    
    # Train model on history (excluding last 7 days)
    t_train = np.arange(len(train_data)).reshape(-1, 1)
    y_train = train_data["Close"]
    model = LinearRegression().fit(t_train, y_train)
    
    # Predict what the AI "thought" would happen in those 7 days
    t_test = np.arange(len(train_data), len(train_data) + 7).reshape(-1, 1)
    predicted_last_7 = model.predict(t_test)

    # --- 3. DISPLAY PERFORMANCE SCORECARD ---
    st.markdown("### 🏆 AI Performance Review (Last 7 Working Days)")
    
    # Create Comparison Table
    comparison_df = pd.DataFrame({
        "Date": actual_last_7["Date"].dt.strftime('%Y-%m-%d'),
        "Actual Price": actual_last_7["Close"].values,
        "AI Prediction": predicted_last_7,
    })
    
    # Calculate Error %
    comparison_df["Difference (%)"] = ((comparison_df["AI Prediction"] - comparison_df["Actual Price"]) / comparison_df["Actual Price"]) * 100
    
    # --- FIXING THE ATTRIBUTE ERROR HERE ---
    # We use .map() instead of .applymap() for Pandas 2.1.0+
    def style_diff(val):
        color = '#ff4b4b' if abs(val) > 5 else '#00ffcc'
        return f'color: {color}; font-weight: bold;'

    styled_table = comparison_df.style.format({
        "Actual Price": "${:,.2f}",
        "AI Prediction": "${:,.2f}",
        "Difference (%)": "{:,.2f}%"
    }).map(style_diff, subset=['Difference (%)']) # Changed from applymap to map

    st.table(styled_table)

    # --- 4. ACCURACY METRICS ---
    st.markdown("---")
    avg_error = comparison_df["Difference (%)"].abs().mean()
    r2 = r2_score(actual_last_7["Close"], predicted_last_7)
    
    # Directional Accuracy Calculation
    direction_correct = 0
    for i in range(1, len(comparison_df)):
        act_up = actual_last_7["Close"].iloc[i] > actual_last_7["Close"].iloc[i-1]
        pred_up = predicted_last_7[i] > predicted_last_7[i-1]
        if act_up == pred_up: direction_correct += 1
    
    dir_acc = int((direction_correct/6)*100)

    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. Deviation", f"{avg_error:.2f}%", help="Lower is better. Shows average gap between AI and Truth.")
    m2.metric("Trend Strength (R²)", f"{max(0, r2*100):.1f}%", help="Closer to 100% means the asset is following a perfect linear path.")
    m3.metric("Directional Accuracy", f"{dir_acc}%", help="How often the AI correctly guessed 'Up' vs 'Down'.")

    # --- 5. FUTURE 7-DAY FORECAST ---
    st.markdown("---")
    st.markdown("### 🚀 Live 7-Day Future Forecast")
    
    # Use ALL data for real future forecast
    result = get_forecast_summary(coin_df, amount, 7)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Target Price", f"${result['predicted_price']:.2f}")
    f2.metric("Portfolio Goal", f"${result['expected_value']:.2f}")
    
    # Calculate delta for the metric
    growth = result['profit_pct']
    f3.metric("Growth Potential", f"{growth:.2f}%", delta=f"{growth:.2f}%")

    # --- 6. FOOTER GUIDE ---
    with st.expander("📝 Why do we show the 'Last 7 Days'?"):
        st.write("""
        This is called **Backtesting**. By showing you the AI's performance on data that has already happened, 
        we provide transparency. 
        - If the **Avg. Deviation** is high (>10%), use caution; the market is too volatile for linear models.
        - If the **Directional Accuracy** is high (>60%), the model is a reliable tool for trend-following strategies.
        """)
