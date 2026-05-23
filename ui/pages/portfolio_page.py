import streamlit as st
import pandas as pd
import plotly.express as px
from db.models import add_holding, get_holdings

def render_portfolio(df):
    st.markdown("# 👤 Portfolio Manager")

    email = st.session_state.get("email")
    # Retrieve live prices updated in app.py
    live_prices = st.session_state.get("prices", {})

    # ==========================================
    # 1. ADD INVESTMENT UI
    # ==========================================
    with st.expander("➕ Add New Investment", expanded=True):
        col1, col2, col3 = st.columns(3)

        available_coins = sorted(df["Crypto"].unique()) if "Crypto" in df.columns else []
        
        coin = col1.selectbox("Crypto Asset", available_coins)
        amount_invested = col2.number_input("Investment Amount ($)", min_value=0.0, value=1000.0)
        date = col3.date_input("Investment Date")

        if st.button("Add to Portfolio", type="primary"):
            # Ensure date is stored as a standard YYYY-MM-DD string
            add_holding(email, coin, amount_invested, str(date))
            st.success(f"Success: Added {coin} investment!")
            st.rerun()

    # ==========================================
    # 2. DATA PROCESSING & CALCULATIONS
    # ==========================================
    data = get_holdings(email)

    if not data:
        st.info("Your portfolio is empty. Add an investment above to see performance tracking.")
        return

    # Create base dataframe from DB: [Crypto, Amount, Date]
    portfolio = pd.DataFrame(data, columns=["Crypto", "Amount Invested", "Date"])

    def calculate_metrics(row):
        symbol = row["Crypto"]
        invested = row["Amount Invested"]
        # Convert user's purchase date to a pandas timestamp for comparison
        buy_date = pd.to_datetime(row["Date"])
        
        try:
            # Prepare historical data: ensure Date is datetime and sorted
            hist_df = df.copy()
            hist_df['Date'] = pd.to_datetime(hist_df['Date'])
            
            # Filter for the specific coin's history
            coin_hist = hist_df[hist_df['Crypto'] == symbol].sort_values('Date')
            
            if not coin_hist.empty:
                # FIX: Find the price on OR before the purchase date (Closest Match)
                # This prevents the "Same Price" bug if the exact date is missing from CSV
                mask = coin_hist['Date'] <= buy_date
                
                if mask.any():
                    # Take the most recent price available before or on that date
                    buy_price = float(coin_hist[mask].iloc[-1]['Close'])
                else:
                    # If purchase date is earlier than our oldest data, take the oldest price
                    buy_price = float(coin_hist.iloc[0]['Close'])
            else:
                # If no history exists for this coin at all
                buy_price = live_prices.get(symbol, 0)

        except Exception:
            buy_price = live_prices.get(symbol, 0)

        # Get current live price from session state
        current_price = float(live_prices.get(symbol, buy_price))
        
        # Calculate tokens and gains
        tokens = invested / buy_price if buy_price > 0 else 0
        current_value = tokens * current_price
        profit = current_value - invested
        pct_change = (profit / invested * 100) if invested > 0 else 0
        
        return pd.Series([buy_price, current_price, profit, pct_change])

    # Apply the logic to create new columns
    portfolio[["Buy Price", "Current Price", "Profit", "% Profit/Loss"]] = portfolio.apply(calculate_metrics, axis=1)

    # ==========================================
    # 3. UI DISPLAY
    # ==========================================
    
    # Summary Metrics Row
    total_inv = portfolio["Amount Invested"].sum()
    total_prof = portfolio["Profit"].sum()
    total_roi = (total_prof / total_inv * 100) if total_inv > 0 else 0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Invested", f"${total_inv:,.2f}")
    m2.metric("Total Profit/Loss", f"${total_prof:,.2f}", delta=f"{total_roi:.2f}%")
    m3.metric("Current Portfolio Value", f"${(total_inv + total_prof):,.2f}")

    st.subheader("Current Holdings Performance")
    
    display_cols = ["Crypto", "Amount Invested", "Buy Price", "Current Price", "Profit", "% Profit/Loss", "Date"]
    
    st.dataframe(
        portfolio[display_cols],
        column_config={
            "Amount Invested": st.column_config.NumberColumn(format="$%.2f"),
            "Buy Price": st.column_config.NumberColumn(format="$%.2f"),
            "Current Price": st.column_config.NumberColumn(format="$%.2f"),
            "Profit": st.column_config.NumberColumn(format="$%.2f"),
            "% Profit/Loss": st.column_config.NumberColumn(format="%.2f%%"),
        },
        use_container_width=True,
        hide_index=True
    )

    # Allocation Chart
    st.subheader("Portfolio Allocation")
    pie = px.pie(portfolio, values='Amount Invested', names='Crypto', hole=0.4, template="plotly_dark")
    st.plotly_chart(pie, use_container_width=True)

    # NEW USER DESCRIPTION
    with st.expander("📖 Help: Understanding your Portfolio"):
        st.write("""
        - **Buy Price:** The price of the coin on the day you purchased it. If you picked a date where the market was closed or data was missing, we use the *closest previous recorded price*.
        - **Current Price:** The real-time price fetched from live market data.
        - **Profit/Loss:** Calculated by comparing how much your tokens are worth now versus what you paid for them.
        """)
