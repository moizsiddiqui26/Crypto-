import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# --- THE FIX: Robust Path Discovery ---
# This identifies the 'crypto-' root folder and adds it to the system path
dir_path = os.path.dirname(os.path.realpath(__file__))
# Move up 2 levels (from pages/ to ui/ to root)
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))

if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Import models using the newly established path
try:
    from db.models import add_holding, get_holdings, sell_holding
except ImportError:
    st.error("Could not find the database modules. Please ensure your folder structure is correct.")

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    if not email:
        st.warning("Please log in to manage your holdings.")
        return

    # ==========================================
    # 🛒 TRANSACTION INTERFACE (BUY & SELL)
    # ==========================================
    with st.expander("➕ / ➖ New Transaction (Buy/Sell)", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        action = c1.radio("Action", ["Buy", "Sell"])
        coin = c2.selectbox("Select Asset", sorted(df["Crypto"].unique()))
        cash_amount = c3.number_input("Amount ($)", min_value=0.0, step=10.0)
        date = c4.date_input("Transaction Date")

        if st.button("Confirm Transaction", use_container_width=True):
            if cash_amount <= 0:
                st.error("Please enter an amount greater than 0.")
            else:
                if action == "Buy":
                    add_holding(email, coin, cash_amount, str(date))
                    st.success(f"Successfully added ${cash_amount:,.2f} to {coin}!")
                else:
                    # Check current cash balance for this coin before selling
                    data = get_holdings(email)
                    temp_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
                    current_bal = temp_df[temp_df["Crypto"] == coin]["Amount"].sum() if not temp_df.empty else 0
                    
                    if cash_amount > current_bal:
                        st.error(f"Insufficient funds! You only have ${current_bal:,.2f} of {coin} available.")
                    else:
                        sell_holding(email, coin, cash_amount, str(date))
                        st.warning(f"Successfully sold ${cash_amount:,.2f} of {coin}!")
                st.rerun()

    # ==========================================
    # 📊 LOGIC: CALCULATING QUANTITY & TOTALS
    # ==========================================
    raw_data = get_holdings(email)
    if not raw_data:
        st.info("Your portfolio is currently empty. Add your first transaction above!")
        return

    # Convert database rows to DataFrame
    all_tx = pd.DataFrame(raw_data, columns=["Crypto", "Amount", "Date"])
    all_tx["Date"] = pd.to_datetime(all_tx["Date"])
    
    summary_data = []
    
    # Group by coin to calculate weighted averages and total units
    for c in all_tx["Crypto"].unique():
        coin_tx = all_tx[all_tx["Crypto"] == c]
        net_cash_invested = coin_tx["Amount"].sum() # Total $ currently in this coin (Buys - Sells)
        
        total_units = 0
        total_buy_cost = 0 # Used for Average Price calculation
        
        for _, row in coin_tx.iterrows():
            # Find the price of the coin at the specific time of this transaction
            # Using price history 'df' provided to the function
            hist_match = df[(df["Crypto"] == c) & (pd.to_datetime(df["Date"]) <= row["Date"])]
            
            # Use the price from that date; fallback to earliest price if date is before dataset
            price_at_tx = hist_match.iloc[-1]["Close"] if not hist_match.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            # Calculate how many units were bought/sold with that amount of cash
            units = row["Amount"] / price_at_tx
            total_units += units
            
            # Only BUYS contribute to the weighted average cost basis
            if row["Amount"] > 0:
                total_buy_cost += row["Amount"]

        current_price = df[df["Crypto"] == c].iloc[-1]["Close"]
        current_value = total_units * current_price
        avg_buy_price = total_buy_cost / total_units if total_units > 0 else 0
        
        # Only show the asset if the user still owns a significant amount
        if total_units > 0.0001:
            summary_data.append({
                "Asset": c,
                "Quantity": total_units,
                "Avg Buy Price": avg_buy_price,
                "Current Price": current_price,
                "Invested ($)": net_cash_invested,
                "Value ($)": current_value,
                "P/L ($)": current_value - net_cash_invested
            })

    if not summary_data:
        st.info("No active holdings (all assets have been sold).")
        return

    final_df = pd.DataFrame(summary_data)

    # ==========================================
    # 💎 PROFESSIONAL UI DISPLAY
    # ==========================================
    st.markdown("### 📋 Portfolio Holdings")
    st.dataframe(
        final_df.style.format({
            "Quantity": "{:.6f}",
            "Avg Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Invested ($)": "${:,.2f}",
            "Value ($)": "${:,.2f}",
            "P/L ($)": "${:,.2f}"
        }).applymap(lambda x: 'color: #00ffcc;' if x > 0 else 'color: #ff4b4b;', subset=['P/L ($)']),
        use_container_width=True,
        hide_index=True
    )

    # --- UPDATED EXECUTIVE TOTALS ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    
    total_port_value = final_df["Value ($)"].sum()
    total_port_invested = final_df["Invested ($)"].sum()
    net_port_profit = total_port_value - total_port_invested
    
    # Calculate Profit % safely
    profit_pct = (net_port_profit / total_port_invested * 100) if total_port_invested != 0 else 0
    
    m1.metric("Total Portfolio Value", f"${total_port_value:,.2f}")
    m2.metric("Total Invested", f"${total_port_invested:,.2f}")
    m3.metric("Net Profit/Loss", f"${net_port_profit:,.2f}", delta=f"{profit_pct:.2f}%")

    # --- VISUALS ---
    fig = px.pie(final_df, values='Value ($)', names='Asset', 
                 title='Asset Allocation', hole=0.5, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
