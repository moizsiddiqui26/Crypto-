import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# --- THE FIX: Robust Path Discovery ---
# This finds the 'crypto-' root folder and adds it to the system path
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))
if root_path not in sys.path:
    sys.path.append(root_path)

# Now try importing using the root-relative path
try:
    from db.models import add_holding, get_holdings, sell_holding
except ImportError:
    # Fallback for local development environments
    from db.models import add_holding, get_holdings, sell_holding

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    if not email:
        st.warning("Please log in to manage your holdings.")
        return

    # --- 1. TRANSACTION INTERFACE ---
    with st.expander("➕ / ➖ Buy or Sell Assets", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        action = c1.radio("Action", ["Buy", "Sell"])
        coin = c2.selectbox("Asset", sorted(df["Crypto"].unique()))
        cash_amount = c3.number_input("Amount ($)", min_value=0.0, step=10.0)
        date = c4.date_input("Date")

        if st.button("Execute Transaction", use_container_width=True):
            if cash_amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                if action == "Buy":
                    add_holding(email, coin, cash_amount, str(date))
                    st.success(f"Added ${cash_amount:,.2f} to {coin}")
                else:
                    # Check balance before selling
                    data = get_holdings(email)
                    current_bal = sum([row[1] for row in data if row[0] == coin])
                    if cash_amount > current_bal:
                        st.error(f"Insufficient funds! You only have ${current_bal:,.2f} of {coin}")
                    else:
                        sell_holding(email, coin, cash_amount, str(date))
                        st.warning(f"Sold ${cash_amount:,.2f} of {coin}")
                st.rerun()

    # --- 2. LOGIC: FIXING TOTALS & QUANTITY ---
    data = get_holdings(email)
    if not data:
        st.info("Your portfolio is empty.")
        return

    # Process transactions to get Quantity and Weighted Average
    raw_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    raw_df["Date"] = pd.to_datetime(raw_df["Date"])
    
    summary_data = []
    for c in raw_df["Crypto"].unique():
        coin_tx = raw_df[raw_df["Crypto"] == c]
        net_cash = coin_tx["Amount"].sum() # Total $ currently in this coin
        
        total_qty = 0
        total_buy_cost = 0
        
        for _, row in coin_tx.iterrows():
            # Find price at the specific transaction date
            hist = df[(df["Crypto"] == c) & (pd.to_datetime(df["Date"]) <= row["Date"])]
            price_at_tx = hist.iloc[-1]["Close"] if not hist.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            qty = row["Amount"] / price_at_tx
            total_qty += qty
            if row["Amount"] > 0:
                total_buy_cost += row["Amount"]

        current_price = df[df["Crypto"] == c].iloc[-1]["Close"]
        current_val = total_qty * current_price
        avg_buy_price = total_buy_cost / total_qty if total_qty > 0 else 0
        
        if total_qty > 0.0001: # Don't display assets you no longer own
            summary_data.append({
                "Asset": c,
                "Quantity": total_qty,
                "Avg Buy Price": avg_buy_price,
                "Current Price": current_price,
                "Invested ($)": net_cash,
                "Value ($)": current_val,
                "P/L ($)": current_val - net_invested # FIXED calculation
            })

    if not summary_data:
        st.info("No active holdings.")
        return

    port_df = pd.DataFrame(summary_data)

    # --- 3. DISPLAY ---
    st.markdown("### 📋 Active Holdings")
    st.dataframe(
        port_df.style.format({
            "Quantity": "{:.6f}",
            "Avg Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Invested ($)": "${:,.2f}",
            "Value ($)": "${:,.2f}",
            "P/L ($)": "${:,.2f}"
        }), use_container_width=True, hide_index=True
    )

    # FIXED TOTALS
    total_value = port_df["Value ($)"].sum()
    total_invested = port_df["Invested ($)"].sum()
    net_pl = total_value - total_invested

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Portfolio Value", f"${total_value:,.2f}")
    m2.metric("Total Invested", f"${total_invested:,.2f}")
    m3.metric("Net Profit/Loss", f"${net_pl:,.2f}", delta=f"{(net_pl/total_invested*100):.2f}%" if total_invested != 0 else "0%")
