import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# --- STEP 1: PATH RESOLUTION (FOR STREAMLIT CLOUD) ---
# This ensures that this nested file can see the 'db' and 'services' folders in the root
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from db.models import add_holding, get_holdings, sell_holding
    from services.email_service import send_transaction_notification
except ImportError:
    st.error("🚨 Critical Error: Could not load backend services. Check your folder structure.")

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    
    email = st.session_state.get("email")
    if not email:
        st.warning("Please log in to manage your portfolio.")
        return

    # ==========================================
    # 🛒 TRANSACTION UI (BUY & SELL)
    # ==========================================
    with st.expander("➕ / ➖ New Transaction (Execute Buy or Sell)", expanded=True):
        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        
        action = t_col1.radio("Action", ["Buy", "Sell"], help="Buy adds to holdings. Sell reduces them.")
        coin = t_col2.selectbox("Select Asset", sorted(df["Crypto"].unique()))
        cash_amount = t_col3.number_input("Cash Amount ($)", min_value=0.0, step=50.0)
        date = t_col4.date_input("Transaction Date")

        if st.button("Confirm Transaction", use_container_width=True):
            # Fetch existing data for validation
            raw_data = get_holdings(email)
            holdings_df = pd.DataFrame(raw_data, columns=["Crypto", "Amount", "Date"])
            
            # Calculate current cash balance for this specific coin
            current_balance = holdings_df[holdings_df["Crypto"] == coin]["Amount"].sum() if not holdings_df.empty else 0

            if action == "Sell" and cash_amount > current_balance:
                st.error(f"❌ Insufficient Balance! You only have ${current_balance:.2f} of {coin} available.")
            elif cash_amount <= 0:
                st.error("Please enter a valid amount.")
            else:
                # Update Database
                if action == "Buy":
                    add_holding(email, coin, cash_amount, str(date))
                else:
                    sell_holding(email, coin, cash_amount, str(date))
                
                # Send Email Receipt (if service is connected)
                try:
                    send_transaction_notification(email, coin, action, cash_amount)
                    st.success(f"🚀 {action} Successful! Email receipt sent.")
                except:
                    st.success(f"🚀 {action} Successful!")
                
                st.rerun()

    # ==========================================
    # 📊 MATH: CALCULATING QUANTITIES & TOTALS
    # ==========================================
    data = get_holdings(email)
    if not data:
        st.info("Your portfolio is currently empty. Add your first transaction above!")
        return

    all_tx = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    all_tx["Date"] = pd.to_datetime(all_tx["Date"])
    
    summary_data = []
    
    for c in all_tx["Crypto"].unique():
        coin_tx = all_tx[all_tx["Crypto"] == c]
        net_cash_invested = coin_tx["Amount"].sum() 
        
        total_units = 0
        total_buy_cost = 0 
        
        for _, row in coin_tx.iterrows():
            # Match historical price at transaction date
            hist_match = df[(df["Crypto"] == c) & (pd.to_datetime(df["Date"]) <= row["Date"])]
            price_at_tx = hist_match.iloc[-1]["Close"] if not hist_match.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            units = row["Amount"] / price_at_tx
            total_units += units
            
            if row["Amount"] > 0:
                total_buy_cost += row["Amount"]

        current_price = df[df["Crypto"] == c].iloc[-1]["Close"]
        current_value = total_units * current_price
        avg_buy_price = total_buy_cost / total_units if total_units > 0 else 0
        
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
        st.info("No active holdings found.")
        return

    final_df = pd.DataFrame(summary_data)

    # ==========================================
    # 💎 UPDATED DISPLAY (FIXED FOR PANDAS 2.1+)
    # ==========================================
    st.markdown("### 📋 Active Holdings")
    st.dataframe(
        final_df.style.format({
            "Quantity": "{:.6f}",
            "Avg Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Invested ($)": "${:,.2f}",
            "Value ($)": "${:,.2f}",
            "P/L ($)": "${:,.2f}"
        }).map(lambda x: 'color: #00ffcc;' if x > 0 else 'color: #ff4b4b;', subset=['P/L ($)']),
        use_container_width=True,
        hide_index=True
    )

    # --- EXECUTIVE TOTALS ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    
    total_port_value = final_df["Value ($)"].sum()
    total_port_invested = final_df["Invested ($)"].sum()
    net_port_profit = total_port_value - total_port_invested
    profit_pct = (net_port_profit / total_port_invested * 100) if total_port_invested != 0 else 0
    
    m1.metric("Total Portfolio Value", f"${total_port_value:,.2f}")
    m2.metric("Total Invested", f"${total_port_invested:,.2f}")
    m3.metric("Net Profit/Loss", f"${net_port_profit:,.2f}", delta=f"{profit_pct:.2f}%")

    # --- ALLOCATION CHART ---
    fig = px.pie(final_df, values='Value ($)', names='Asset', 
                 title='Asset Allocation', hole=0.5, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
