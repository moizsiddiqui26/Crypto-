import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, sell_holding, get_holdings

# FIXED: sys.path allows importing from the root directory when in a sub-folder
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from email_service import send_transaction_notification

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    # --- 1. TRANSACTION INTERFACE (BUY/SELL) ---
    with st.expander("➕ / ➖ New Transaction", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        action = col1.radio("Action", ["Buy", "Sell"])
        coin = col2.selectbox("Asset", sorted(df["Crypto"].unique()))
        amount_usd = col3.number_input("Amount ($)", min_value=0.0, step=10.0)
        date = col4.date_input("Date")

        if st.button("Confirm Order", use_container_width=True):
            # Fetch current data to check available balance
            current_raw = get_holdings(email)
            temp_df = pd.DataFrame(current_raw, columns=["Crypto", "Amount", "Date"])
            balance = temp_df[temp_df["Crypto"] == coin]["Amount"].sum() if not temp_df.empty else 0

            if action == "Sell" and amount_usd > balance:
                st.error(f"❌ Insufficient Funds! You only have ${balance:.2f} of {coin}.")
            elif amount_usd <= 0:
                st.error("Please enter a valid amount.")
            else:
                if action == "Buy":
                    add_holding(email, coin, amount_usd, str(date))
                else:
                    sell_holding(email, coin, amount_usd, str(date))
                
                # Notification Email
                send_transaction_notification(email, coin, action, amount_usd)
                st.success(f"✅ {action} Successful! Email receipt sent.")
                st.rerun()

    # --- 2. PROFESSIONAL METRIC CALCULATION ---
    raw_data = get_holdings(email)
    if not raw_data:
        st.info("Portfolio is empty.")
        return

    raw_df = pd.DataFrame(raw_data, columns=["Crypto", "Amount", "Date"])
    portfolio_stats = []

    for c in raw_df["Crypto"].unique():
        coin_tx = raw_df[raw_df["Crypto"] == c]
        net_cash = coin_tx["Amount"].sum()
        
        total_qty = 0
        total_buy_cost = 0
        
        for _, row in coin_tx.iterrows():
            # Get historical price at the time of purchase
            hist = df[(df["Crypto"] == c) & (df["Date"] <= row["Date"])]
            price_then = hist.iloc[-1]["Close"] if not hist.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            qty = row["Amount"] / price_then
            total_qty += qty
            if row["Amount"] > 0: # Only Buys contribute to the Average Price
                total_buy_cost += row["Amount"]

        avg_price = total_buy_cost / total_qty if total_qty > 0 else 0
        current_price = df[df["Crypto"] == c]["Close"].iloc[-1]
        current_val = total_qty * current_price
        
        if total_qty > 0.0001: # Only show active holdings
            portfolio_stats.append({
                "Asset": c,
                "Qty": round(total_qty, 4),
                "Avg Buy Price": avg_price,
                "Current Price": current_price,
                "Value": current_val,
                "Profit": current_val - net_cash
            })

    if not portfolio_stats:
        st.info("No active holdings.")
        return

    # --- 3. DISPLAY SUMMARY ---
    p_df = pd.DataFrame(portfolio_stats)
    st.dataframe(p_df.style.format({
        "Avg Buy Price": "${:,.2f}",
        "Current Price": "${:,.2f}",
        "Value": "${:,.2f}",
        "Profit": "${:,.2f}"
    }), use_container_width=True, hide_index=True)

    m1, m2, m3 = st.columns(3)
    total_val = p_df["Value"].sum()
    total_profit = p_df["Profit"].sum()
    m1.metric("Total Portfolio Value", f"${total_val:,.2f}")
    m2.metric("Total Profit/Loss", f"${total_profit:,.2f}", delta=f"${total_profit:,.2f}")
    m3.metric("Assets", len(p_df))
