import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# --- PATH FIX FOR STREAMLIT CLOUD ---
# Adds the root directory to the python path so modules like 'db' can be found
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from db.models import add_holding, get_holdings, sell_holding  # Ensure sell_holding is imported

def render_portfolio(df):
    st.markdown('<div class="section-title">👤 Professional Portfolio</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    if not email:
        st.warning("Please log in to manage your portfolio.")
        return

    # ==========================================
    # 🛒 TRANSACTION INTERFACE (BUY & SELL)
    # ==========================================
    with st.expander("➕ / ➖ New Transaction", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        action = col1.radio("Action", ["Buy", "Sell"])
        coin = col2.selectbox("Crypto", sorted(df["Crypto"].unique()))
        amount = col3.number_input("Cash Amount ($)", min_value=0.0)
        date = col4.date_input("Date")

        if st.button("Execute Transaction", use_container_width=True):
            if amount <= 0:
                st.error("Please enter an amount greater than 0.")
            else:
                if action == "Buy":
                    add_holding(email, coin, amount, str(date))
                    st.success(f"Added ${amount:,.2f} of {coin}!")
                else:
                    # Validate if user has enough balance to sell
                    current_data = get_holdings(email)
                    temp_df = pd.DataFrame(current_data, columns=["Crypto", "Amount", "Date"])
                    balance = temp_df[temp_df["Crypto"] == coin]["Amount"].sum() if not temp_df.empty else 0
                    
                    if amount > balance:
                        st.error(f"Insufficient funds! Current {coin} balance: ${balance:,.2f}")
                    else:
                        sell_holding(email, coin, amount, str(date))
                        st.warning(f"Sold ${amount:,.2f} of {coin}!")
                st.rerun()

    # ==========================================
    # 📊 CALCULATE METRICS & QUANTITY
    # ==========================================
    data = get_holdings(email)
    if not data:
        st.info("No investments yet.")
        return

    raw_tx = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    raw_tx["Date"] = pd.to_datetime(raw_tx["Date"])
    
    summary_list = []
    for coin_name in raw_tx["Crypto"].unique():
        coin_tx = raw_tx[raw_tx["Crypto"] == coin_name]
        net_cash = coin_tx["Amount"].sum()
        
        total_qty = 0
        total_buy_cost = 0
        
        for _, row in coin_tx.iterrows():
            # Find price on transaction date
            hist_df = df[(df["Crypto"] == coin_name) & (pd.to_datetime(df["Date"]) <= row["Date"])]
            price_at_tx = hist_df.iloc[-1]["Close"] if not hist_df.empty else df[df["Crypto"]==coin_name]["Close"].iloc[0]
            
            qty = row["Amount"] / price_at_tx
            total_qty += qty
            if row["Amount"] > 0:
                total_buy_cost += row["Amount"]

        current_price = df[df["Crypto"] == coin_name].iloc[-1]["Close"]
        current_val = total_qty * current_price
        avg_buy_price = total_buy_cost / total_qty if total_qty > 0 else 0
        
        if total_qty > 0.0001:
            summary_list.append({
                "Crypto": coin_name,
                "Quantity": total_qty,
                "Avg Buy Price": avg_buy_price,
                "Current Price": current_price,
                "Invested ($)": net_cash,
                "Current Value ($)": current_val,
                "Profit ($)": current_val - net_cash
            })

    if not summary_list:
        st.info("No active holdings.")
        return

    portfolio_df = pd.DataFrame(summary_list)

    # ==========================================
    # 💎 DISPLAY HOLDINGS TABLE
    # ==========================================
    st.markdown("### 📋 Active Holdings")
    st.dataframe(
        portfolio_df.style.format({
            "Quantity": "{:.6f}",
            "Avg Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Invested ($)": "${:,.2f}",
            "Current Value ($)": "${:,.2f}",
            "Profit ($)": "${:,.2f}"
        }), 
        use_container_width=True, 
        hide_index=True
    )

    # ==========================================
    # 📈 TOTAL SUMMARY METRICS
    # ==========================================
    t_invested = portfolio_df["Invested ($)"].sum()
    t_value = portfolio_df["Current Value ($)"].sum()
    t_profit = t_value - t_invested
    p_pct = (t_profit / t_invested * 100) if t_invested > 0 else 0

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Invested", f"${t_invested:,.2f}")
    m2.metric("Portfolio Value", f"${t_value:,.2f}")
    m3.metric("Net Profit", f"${t_profit:,.2f}", delta=f"{p_pct:.2f}%")
