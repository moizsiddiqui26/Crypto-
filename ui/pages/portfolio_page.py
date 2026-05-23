import streamlit as st
import pandas as pd
from db.models import add_holding, get_holdings

def render_portfolio(df):
    st.markdown("# 👤 Portfolio Manager")
    email = st.session_state.get("email")
    live_prices = st.session_state.get("prices", {})

    with st.expander("➕ Add New Investment", expanded=True):
        col1, col2, col3 = st.columns(3)
        available_coins = sorted(df["Crypto"].unique())
        coin = col1.selectbox("Crypto Asset", available_coins)
        amount = col2.number_input("Investment Amount ($)", min_value=0.0, value=1000.0)
        date = col3.date_input("Investment Date")

        if st.button("Add to Portfolio", type="primary"):
            add_holding(email, coin, amount, str(date))
            st.success(f"Added {coin}!")
            st.rerun()

    data = get_holdings(email)
    if not data:
        st.info("Portfolio empty.")
        return

    portfolio = pd.DataFrame(data, columns=["Crypto", "Amount Invested", "Date"])

    def calculate_metrics(row):
        symbol = row["Crypto"]
        invested = row["Amount Invested"]
        buy_date_str = str(row["Date"]) # Format as YYYY-MM-DD
        
        # Ensure hist_df dates are also strings for exact matching
        hist_df = df.copy()
        hist_df['Date'] = pd.to_datetime(hist_df['Date']).dt.strftime('%Y-%m-%d')
        
        match = hist_df[(hist_df['Crypto'] == symbol) & (hist_df['Date'] == buy_date_str)]
        
        # FIX: Only use live price as fallback if history is missing
        if not match.empty:
            buy_price = float(match.iloc[0]['Close'])
        else:
            # Look for the earliest price for that coin in the DB
            coin_hist = hist_df[hist_df['Crypto'] == symbol]
            buy_price = float(coin_hist.iloc[0]['Close']) if not coin_hist.empty else live_prices.get(symbol, 0)

        current_price = live_prices.get(symbol, buy_price)
        profit = ((invested / buy_price) * current_price) - invested if buy_price > 0 else 0
        pct = (profit / invested * 100) if invested > 0 else 0
        
        return pd.Series([buy_price, current_price, profit, pct])

    portfolio[["Buy Price", "Current Price", "Profit", "% Profit/Loss"]] = portfolio.apply(calculate_metrics, axis=1)
    st.dataframe(portfolio, use_container_width=True, hide_index=True)
