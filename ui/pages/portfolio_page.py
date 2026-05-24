import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# Robust path handling to find root directory files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from email_service import send_transaction_notification
from db.models import add_holding, sell_holding, get_holdings

def render_portfolio(df):
    st.markdown('<div class="section-title">👤 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    # --- TRANSACTION INTERFACE ---
    with st.expander("➕ / ➖ Buy or Sell Assets", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        action = c1.radio("Action", ["Buy", "Sell"])
        coin = c2.selectbox("Crypto", df["Crypto"].unique())
        amount = c3.number_input("Amount ($)", min_value=0.0)
        date = c4.date_input("Date")

        if st.button("Confirm Order", use_container_width=True):
            # Fetch current balance for sell validation
            existing = get_holdings(email)
            balance_df = pd.DataFrame(existing, columns=["Crypto", "Amt", "D"])
            current_bal = balance_df[balance_df["Crypto"] == coin]["Amt"].sum() if not balance_df.empty else 0

            if action == "Sell" and amount > current_bal:
                st.error(f"Insufficient funds! You only have ${current_bal:.2f} of {coin}.")
            else:
                if action == "Buy":
                    add_holding(email, coin, amount, str(date))
                else:
                    sell_holding(email, coin, amount, str(date))
                
                send_transaction_notification(email, coin, action, amount)
                st.success(f"{action} successful! Email receipt sent.")
                st.rerun()

    # --- CALCULATE PROFESSIONAL METRICS ---
    raw_data = get_holdings(email)
    if not raw_data:
        st.info("Your portfolio is currently empty.")
        return

    all_tx = pd.DataFrame(raw_data, columns=["Crypto", "Amount", "Date"])
    summary_data = []

    for c in all_tx["Crypto"].unique():
        coin_tx = all_tx[all_tx["Crypto"] == c]
        net_invested = coin_tx["Amount"].sum()
        
        total_qty = 0
        total_buy_cost = 0
        
        for _, row in coin_tx.iterrows():
            # Get price on the day of transaction
            hist = df[(df["Crypto"] == c) & (pd.to_datetime(df["Date"]) <= pd.to_datetime(row["Date"]))]
            price_then = hist.iloc[-1]["Close"] if not hist.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            qty = row["Amount"] / price_then
            total_qty += qty
            if row["Amount"] > 0: # Only Buys affect Average Price
                total_buy_cost += row["Amount"]

        avg_price = total_buy_cost / total_qty if total_qty > 0 else 0
        curr_price = df[df["Crypto"] == c]["Close"].iloc[-1]
        
        if total_qty > 0.001:
            summary_data.append({
                "Crypto": c,
                "Holdings": round(total_qty, 4),
                "Avg. Buy Price": avg_price,
                "Current Price": curr_price,
                "Current Value": total_qty * curr_price,
                "Net P/L ($)": (total_qty * curr_price) - net_invested
            })

    # --- DISPLAY ---
    if summary_data:
        port_df = pd.DataFrame(summary_data)
        st.dataframe(port_df.style.format("${:,.2f}", subset=["Avg. Buy Price", "Current Price", "Current Value", "Net P/L ($)"]), use_container_width=True)
        
        m1, m2, m3 = st.columns(3)
        total_val = port_df["Current Value"].sum()
        m1.metric("Total Value", f"${total_val:,.2f}")
        m2.metric("Active Assets", len(port_df))
        m3.metric("Status", "LIVE")
