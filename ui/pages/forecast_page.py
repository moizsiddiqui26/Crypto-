import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    st.markdown("# 🔮 AI Price Forecast")
    
    # --- NEW USER INTRO ---
    st.info("💡 **Welcome to AI Forecasting!** We use Machine Learning to analyze price history and predict where the market might go in the next 7 days.")

    # Selection Logic
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        coin = st.selectbox("Select Asset to Predict", sorted(df["Crypto"].unique()))
    with col_sel2:
        amount = st.number_input("If I invest this much ($):", value=1000.0)

    # Forecasting Logic
    coin_df = df[df["Crypto"] == coin]
    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        # Results metrics
        st.markdown("### 🎯 Prediction Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        m2.metric("Expected Portfolio Value", f"${result['expected_value']:.2f}")
        m3.metric("Estimated Growth (%)", f"{result['profit_pct']:.2f}%", delta=f"{result['profit_pct']:.2f}%")

        # ---------------------------------------------------------
        # NEW SECTION: HOW THE AI THINKS
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("📊 How the AI 'Thinks'")
        st.write("The AI looks at the **blue 'Past' line** (Historical Data) to project the **dotted 'Future' line** (Prediction).")

        # Visualizing the "Thinking Process" with a Chart
        # We take the last 30 days of history and append the 7-day prediction
        history = coin_df.tail(30).copy()
        
        fig = go.Figure()

        # 1. Plot the "Past" Line (Historical Data)
        fig.add_trace(go.Scatter(
            x=history['Date'], y=history['Close'],
            name='Historical (Past)',
            line=dict(color='#3861FB', width=3)
        ))

        # 2. Plot the "Future" Line (Dotted Prediction)
        # Create a tiny 2-point dataframe to connect the last price to the predicted price
        last_date = pd.to_datetime(history['Date'].iloc[-1])
        future_date = last_date + pd.Timedelta(days=7)
        
        fig.add_trace(go.Scatter(
            x=[last_date, future_date], 
            y=[history['Close'].iloc[-1], result['predicted_price']],
            name='AI Prediction (Future)',
            line=dict(color='#858ca2', width=3, dash='dot')
        ))

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Timeline",
            yaxis_title="Price ($)",
            hovermode="x unified",
            margin=dict(l=0, r=0, t=20, b=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        

        # Beginner's Guide Expanders
        with st.expander("📚 Beginner's Dictionary: Prediction Terms"):
            st.markdown("""
            - **Historical Trend:** The 'memory' of the AI. It looks for recurring shapes in the blue line.
            - **Dotted Line (Projection):** This is the AI's 'best guess' based on the patterns it found.
            - **Risk Factor:** The further into the future we look, the more the 'dotted line' can be affected by unexpected news.
            """)
            
    else:
        st.error("Not enough data to calculate a forecast for this coin.")
