import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.forecast_engine import get_forecast_summary
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    st.markdown("# 🔮 AI Price Intelligence & Backtesting")
    
    st.markdown("""
        <div style="background: rgba(0, 255, 204, 0.05); padding: 20px; border-radius: 12px; border-left: 5px solid #00ffcc; margin-bottom: 30px;">
            <h4 style="margin:0; color: #00ffcc;">💡 Intelligence Tip for New Users</h4>
            <p style="margin:5px 0 0 0; color: #94A3B8; font-size: 14px;">
                <b>Watch the Trend:</b> If the AI Prediction and Actual Price move in the same direction, the model is successfully capturing market momentum.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Asset Selection
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        coin = st.selectbox("Select Asset to Analyze", sorted(df["Crypto"].unique()))
    with col_sel2:
        amount = st.number_input("Hypothetical Investment ($):", value=1000.0)

    # --- DATA FIX: Ensure unique daily prices ---
    # Group by date to ensure we don't have multiple entries for the same day
    coin_df = df[df["Crypto"] == coin].copy()
    coin_df['Date'] = pd.to_datetime(coin_df['Date']).dt.normalize()
    coin_df = coin_df.groupby('Date')['Close'].mean().reset_index().sort_values("Date")
    
    if len(coin_df) < 14:
        st.warning("⚠️ Insufficient data for 7-day backtesting.")
        return

    # --- BACKTESTING LOGIC ---
    train_data = coin_df.iloc[:-7].reset_index(drop=True)
    actual_last_7 = coin_df.iloc[-7:].reset_index(drop=True)
    
    # Train model on historical data
    X_train = np.arange(len(train_data)).reshape(-1, 1)
    y_train = train_data["Close"]
    model = LinearRegression().fit(X_train, y_train)
    
    # Predict the last 7 days
    X_test = np.arange(len(train_data), len(train_data) + 7).reshape(-1, 1)
    predicted_last_7 = model.predict(X_test)

    # --- DISPLAY TABLE ---
    st.markdown("### 🏆 AI Performance Review (Last 7 Working Days)")
    
    # Create the comparison dataframe with CORRECT distinct dates
    comparison_df = pd.DataFrame({
        "Date": actual_last_7["Date"].dt.strftime('%Y-%m-%d'),
        "Actual Price": actual_last_7["Close"].values,
        "AI Prediction": predicted_last_7,
    })
    
    comparison_df["Difference (%)"] = ((comparison_df["AI Prediction"] - comparison_df["Actual Price"]) / comparison_df["Actual Price"]) * 100
    
    def style_diff(val):
        color = '#ff4b4b' if abs(val) > 5 else '#00ffcc'
        return f'color: {color}; font-weight: bold;'

    styled_table = comparison_df.style.format({
        "Actual Price": "${:,.2f}",
        "AI Prediction": "${:,.2f}",
        "Difference (%)": "{:,.2f}%"
    }).map(style_diff, subset=['Difference (%)'])

    st.table(styled_table)

    # --- ACCURACY METRICS ---
    st.markdown("---")
    avg_error = comparison_df["Difference (%)"].abs().mean()
    
    # Simple Directional Accuracy check
    correct_dir = 0
    for i in range(1, len(comparison_df)):
        actual_up = comparison_df["Actual Price"].iloc[i] > comparison_df["Actual Price"].iloc[i-1]
        pred_up = comparison_df["AI Prediction"].iloc[i] > comparison_df["AI Prediction"].iloc[i-1]
        if actual_up == pred_up: correct_dir += 1
    
    dir_acc = int((correct_dir / 6) * 100)

    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. Deviation", f"{avg_error:.2f}%")
    m2.metric("Directional Accuracy", f"{dir_acc}%")
    m3.metric("Model Status", "RELIABLE" if avg_error < 10 else "VOLATILE")

    # --- FUTURE FORECAST ---
    st.markdown("---")
    st.markdown("### 🚀 Live Future Forecast")
    
    # Re-using the original dataframe structure for the engine
    full_coin_df = df[df["Crypto"] == coin].sort_values("Date")
    result = get_forecast_summary(full_coin_df, amount, 7)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Target Price", f"${result['predicted_price']:.2f}")
    f2.metric("Portfolio Goal", f"${result['expected_value']:.2f}")
    f3.metric("Growth Potential", f"{result['profit_pct']:.2f}%", delta=f"{result['profit_pct']:.2f}%")
