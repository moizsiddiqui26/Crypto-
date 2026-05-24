import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, sell_holding, get_holdings
# FIXED: Importing the correct function names from email_service
from email_service import send_transaction_notification

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    # --- 1. TRANSACTION INTERFACE ---
    with st.expander("➕ / ➖ New Transaction (Buy/Sell)", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        action = col1.radio("Action", ["Buy", "Sell"])
        coin = col2.selectbox("Crypto", sorted(df["Crypto"].unique()))
        amount_usd = col3.number_input("Cash Amount ($)", min_value=0.0, step=10.0)
        date = col4.date_input("Date")

        if st.button("Execute Transaction", use_container_width=True):
            # Check current balance for sells
            current_data = get_holdings(email)
            temp_df = pd.DataFrame(current_data, columns=["Crypto", "Amount", "Date"])
            balance = temp_df[temp_df["Crypto"] == coin]["Amount"].sum() if not temp_df.empty else 0

            if action == "Sell" and amount_usd > balance:
                st.error(f"❌ Insufficient Funds! You only have ${balance:.2f} of {coin}.")
            elif amount_usd <= 0:
                st.error("Please enter an amount greater than 0.")
            else:
                if action == "Buy":
                    add_holding(email, coin, amount_usd, str(date))
                else:
                    sell_holding(email, coin, amount_usd, str(date))
                
                # Send Email Notification
                send_transaction_notification(email, coin, action, amount_usd)
                st.success(f"✅ {action} Successful! Email receipt sent.")
                st.rerun()

    # --- 2. CALCULATE PROFESSIONAL METRICS ---
    data = get_holdings(email)
    if not data:
        st.info("Your portfolio is currently empty.")
        return

    # Process transactions to find Average Price and Quantity
    raw_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    summary_data = []

    for c in raw_df["Crypto"].unique():
        coin_tx = raw_df[raw_df["Crypto"] == c]
        total_invested = coin_tx["Amount"].sum()
        
        # Calculate quantity and cost basis
        total_qty = 0
        total_cost_basis = 0
        
        for _, row in coin_tx.iterrows():
            # Get historical price at that date
            hist = df[(df["Crypto"] == c) & (df[ "Date"] <= row["Date"])]
            price_at_time = hist.iloc[-1]["Close"] if not hist.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            qty = row["Amount"] / price_at_time
            total_qty += qty
            if row["Amount"] > 0: # Only Buys affect Average Price
                total_cost_basis += row["Amount"]

        avg_buy_price = total_cost_basis / total_qty if total_qty > 0 else 0
        current_price = df[df["Crypto"] == c]["Close"].iloc[-1]
        current_value = total_qty * current_price
        
        if total_qty > 0.0001: # Filter out sold-off positions
            summary_data.append({
                "Crypto": c,
                "Holdings": round(total_qty, 4),
                "Avg. Buy Price": f"${avg_buy_price:,.2f}",
                "Current Price": f"${current_price:,.2f}",
                "Value": current_value,
                "Profit": current_value - total_invested
            })

    if not summary_data:
        st.info("You currently have no active holdings.")
        return

    portfolio_df = pd.DataFrame(summary_data)

    # --- 3. DISPLAY ---
    st.dataframe(portfolio_df, use_container_width=True, hide_index=True)

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    total_val = portfolio_df["Value"].sum()
    total_prof = portfolio_df["Profit"].sum()
    
    m1.metric("Total Value", f"${total_val:,.2f}")
    m2.metric("Net Profit/Loss", f"${total_prof:,.2f}", delta=f"{total_prof:,.2f}")
    m3.metric("Assets Held", len(portfolio_df))

    # Allocation Chart
    fig = px.pie(portfolio_df, values='Value', names='Crypto', 
                 title="Portfolio Allocation", hole=0.4, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
