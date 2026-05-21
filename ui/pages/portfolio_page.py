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

    # Create base dataframe [Crypto, Amount, Date]
    portfolio = pd.DataFrame(data, columns=["Crypto", "Amount Invested", "Date"])
    
    def calculate_metrics(row):
        symbol = row["Crypto"]
        invested = row["Amount Invested"]
        buy_date = pd.to_datetime(row["Date"]).date()
        
        # A. Determine Buy Price (Historical price on the selected date)
        try:
            hist_df = df.copy()
            hist_df['Date'] = pd.to_datetime(hist_df['Date']).dt.date
            # Filter for the specific coin and date
            match = hist_df[(hist_df['Crypto'] == symbol) & (hist_df['Date'] == buy_date)]
            
            if not match.empty:
                buy_price = match.iloc[0]['Close']
            else:
                # Fallback: Use live price if date is today or not in history
                buy_price = live_prices.get(symbol, 0)
        except:
            buy_price = live_prices.get(symbol, 0)

        # B. Get Current Price from live state
        current_price = live_prices.get(symbol, buy_price)
        
        # C. Performance Logic
        # Tokens bought = Total $ / Price at that time
        tokens = invested / buy_price if buy_price > 0 else 0
        current_value = tokens * current_price
        profit = current_value - invested
        pct_change = (profit / invested * 100) if invested > 0 else 0
        
        return pd.Series([buy_price, current_price, profit, pct_change])

    # Apply calculations to create new columns
    portfolio[['Buy Price', 'Current Price', 'Profit', '% Profit/Loss']] = portfolio.apply(calculate_metrics, axis=1)

    # ==========================================
    # 3. DISPLAY TABLE & SUMMARY
    # ==========================================
    
    # Reorder columns for the requested view
    display_cols = ["Crypto", "Amount Invested", "Buy Price", "Current Price", "Profit", "% Profit/Loss", "Date"]
    
    st.subheader("Current Holdings Performance")
    
    # Use st.dataframe with column_config for professional formatting
    st.dataframe(
        portfolio[display_cols],
        column_config={
            "Amount Invested": st.column_config.NumberColumn("Amount Invested", format="$%.2f"),
            "Buy Price": st.column_config.NumberColumn("Buy Price", format="$%.2f"),
            "Current Price": st.column_config.NumberColumn("Current Price", format="$%.2f"),
            "Profit": st.column_config.NumberColumn("Profit ($)", format="$%.2f"),
            "% Profit/Loss": st.column_config.NumberColumn("Change (%)", format="%.2f%%"),
        },
        use_container_width=True,
        hide_index=True
    )

    # Summary Metrics Row
    total_inv = portfolio["Amount Invested"].sum()
    total_prof = portfolio["Profit"].sum()
    total_roi = (total_prof / total_inv * 100) if total_inv > 0 else 0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Invested", f"${total_inv:,.2f}")
    m2.metric("Total Profit/Loss", f"${total_prof:,.2f}", delta=f"{total_roi:.2f}%")
    m3.metric("Current Portfolio Value", f"${(total_inv + total_prof):,.2f}")

    # Allocation Chart
    pie = px.pie(
        portfolio,
        names="Crypto",
        values="Amount Invested",
        title="Asset Allocation (by Investment)",
        template="plotly_dark",
        hole=0.4
    )
    st.plotly_chart(pie, use_container_width=True)
