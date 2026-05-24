import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, sell_holding, get_holdings
from email_service import send_portfolio_summary_email

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    email = st.session_state.get("email")

    # =========================
    # 🛒 TRANSACTION INTERFACE (BUY/SELL)
    # =========================
    with st.expander("➕ / ➖ Add New Transaction", expanded=False):
        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        action = t_col1.radio("Action", ["Buy", "Sell"])
        coin = t_col2.selectbox("Crypto", df["Crypto"].unique())
        cash_amount = t_col3.number_input("Amount ($)", min_value=0.0)
        date = t_col4.date_input("Transaction Date")

        if st.button("Confirm Transaction", use_container_width=True):
            if action == "Buy":
                add_holding(email, coin, cash_amount, str(date))
                st.success(f"Successfully bought ${cash_amount} of {coin}")
                send_portfolio_summary_email(email, pd.DataFrame()) # Trigger Update Email
                st.rerun()
            else:
                # Validation: Check if user has enough to sell (Logic below in Display section)
                # For immediate validation, we fetch current data
                current_data = get_holdings(email)
                holdings_df = pd.DataFrame(current_data, columns=["Crypto", "Amount", "Date"])
                available_cash = holdings_df[holdings_df["Crypto"] == coin]["Amount"].sum()
                
                if cash_amount > available_cash:
                    st.error(f"Insufficient balance! You only have ${available_cash:.2f} worth of {coin} available.")
                else:
                    sell_holding(email, coin, cash_amount, str(date))
                    st.warning(f"Successfully sold ${cash_amount} of {coin}")
                    send_portfolio_summary_email(email, pd.DataFrame()) # Trigger Update Email
                    st.rerun()

    # =========================
    # 📊 CALCULATE PROFESSIONAL METRICS
    # =========================
    raw_data = get_holdings(email)
    if not raw_data:
        st.info("Your portfolio is empty. Start by adding an investment!")
        return

    # Group data by Coin to get Weighted Average and Net Quantity
    summary_list = []
    unique_coins = set([row[0] for row in raw_data])

    for c in unique_coins:
        coin_transactions = [r for r in raw_data if r[0] == c]
        net_invested = sum([r[1] for r in coin_transactions]) # Total cash currently in the coin
        
        # Calculate Weighted Average Price
        total_qty = 0
        total_cost = 0
        for amt, dt in coin_transactions:
            # Get historical price at that date
            hist_price = df[(df["Crypto"] == c) & (df["Date"] <= dt)].iloc[-1]["Close"]
            qty = amt / hist_price
            total_qty += qty
            if amt > 0: # Only Buys affect the average "cost" price
                total_cost += amt
        
        avg_price = total_cost / total_qty if total_qty > 0 else 0
        curr_price = df[df["Crypto"] == c].iloc[-1]["Close"]
        curr_value = total_qty * curr_price
        profit = curr_value - net_invested

        if total_qty > 0.0001: # Hide coins with zero balance
            summary_list.append({
                "Crypto": c,
                "Net Quantity": round(total_qty, 4),
                "Avg. Buy Price": round(avg_price, 2),
                "Current Price": round(curr_price, 2),
                "Total Invested": round(net_invested, 2),
                "Current Value": round(curr_value, 2),
                "Profit ($)": round(profit, 2),
                "Profit (%)": round((profit/net_invested)*100, 2) if net_invested != 0 else 0
            })

    portfolio_df = pd.DataFrame(summary_list)

    # =========================
    # 💎 PROFESSIONAL DISPLAY
    # =========================
    st.dataframe(portfolio_df, use_container_width=True, hide_index=True)

    # Totals
    total_val = portfolio_df["Current Value"].sum()
    total_inv = portfolio_df["Total Invested"].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Portfolio Value", f"${total_val:,.2f}")
    m2.metric("Net Invested", f"${total_inv:,.2f}")
    m3.metric("Net Profit", f"${total_val - total_inv:,.2f}", delta=f"{((total_val-total_inv)/total_inv)*100:.2f}%" if total_inv > 0 else "0%")

    # Pie Chart for Allocation
    fig = px.pie(portfolio_df, values='Current Value', names='Crypto', title='Asset Allocation', hole=.4, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
