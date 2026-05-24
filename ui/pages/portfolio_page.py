import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, sell_holding, get_holdings
import sys
import os

# Ensure the app can find email_service.py in the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from email_service import send_transaction_notification

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    
    email = st.session_state.get("email")
    if not email:
        st.error("Please log in to access your portfolio.")
        return

    # ==========================================
    # 🛒 TRANSACTION INTERFACE (BUY & SELL)
    # ==========================================
    with st.expander("➕ / ➖ New Transaction (Execute Buy or Sell)", expanded=True):
        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        
        action = t_col1.radio("Action", ["Buy", "Sell"], help="Buy adds to your holdings. Sell reduces them.")
        coin = t_col2.selectbox("Select Asset", sorted(df["Crypto"].unique()))
        cash_amount = t_col3.number_input("Cash Amount ($)", min_value=0.0, step=50.0)
        date = t_col4.date_input("Transaction Date")

        if st.button("Confirm Transaction", use_container_width=True):
            # 1. Fetch current data to validate balance
            raw_data = get_holdings(email)
            holdings_df = pd.DataFrame(raw_data, columns=["Crypto", "Amount", "Date"])
            
            # Calculate current cash balance for this specific coin
            current_balance = holdings_df[holdings_df["Crypto"] == coin]["Amount"].sum() if not holdings_df.empty else 0

            if action == "Sell" and cash_amount > current_balance:
                st.error(f"❌ Insufficient Balance! You only have ${current_balance:.2f} of {coin} available to sell.")
            elif cash_amount <= 0:
                st.error("Please enter a valid amount greater than $0.")
            else:
                # 2. Update Database
                if action == "Buy":
                    add_holding(email, coin, cash_amount, str(date))
                    st.success(f"🚀 Successfully purchased ${cash_amount:,.2f} of {coin}!")
                else:
                    sell_holding(email, coin, cash_amount, str(date))
                    st.warning(f"📉 Successfully sold ${cash_amount:,.2f} of {coin}!")
                
                # 3. Send Email Notification
                send_transaction_notification(email, coin, action, cash_amount)
                
                # 4. Refresh UI
                st.rerun()

    # ==========================================
    # 📊 PROFESSIONAL PORTFOLIO CALCULATIONS
    # ==========================================
    raw_holdings = get_holdings(email)
    
    if not raw_holdings:
        st.info("Your portfolio is currently empty. Use the section above to add your first investment.")
        return

    # Convert database rows to DataFrame
    all_tx = pd.DataFrame(raw_holdings, columns=["Crypto", "Amount", "Date"])
    portfolio_summary = []

    # Process each unique coin to find Weighted Average Price and current profit
    for c in all_tx["Crypto"].unique():
        coin_tx = all_tx[all_tx["Crypto"] == c].copy()
        net_cash_invested = coin_tx["Amount"].sum()
        
        total_units = 0
        total_buy_cost = 0
        
        for _, row in coin_tx.iterrows():
            # Find the historical price at the time of THIS transaction
            hist_match = df[(df["Crypto"] == c) & (df["Date"] <= row["Date"])]
            
            # If no historical date matches exactly, use the earliest available price
            price_at_tx = hist_match.iloc[-1]["Close"] if not hist_match.empty else df[df["Crypto"]==c]["Close"].iloc[0]
            
            units_at_tx = row["Amount"] / price_at_tx
            total_units += units_at_tx
            
            # Only BUYS contribute to the cost basis (Average Price)
            if row["Amount"] > 0:
                total_buy_cost += row["Amount"]

        # Final metrics per coin
        avg_buy_price = total_buy_cost / total_units if total_units > 0 else 0
        current_price = df[df["Crypto"] == c]["Close"].iloc[-1]
        current_value = total_units * current_price
        profit_loss = current_value - net_cash_invested
        
        # Only display if the user actually still owns units
        if total_units > 0.0001:
            portfolio_summary.append({
                "Asset": c,
                "Quantity": round(total_units, 4),
                "Avg Buy Price": avg_buy_price,
                "Current Price": current_price,
                "Total Invested": net_cash_invested,
                "Current Value": current_value,
                "P/L ($)": profit_loss,
                "ROI (%)": (profit_loss / net_cash_invested * 100) if net_cash_invested != 0 else 0
            })

    if not portfolio_summary:
        st.warning("All assets have been sold. Your active portfolio is empty.")
        return

    final_df = pd.DataFrame(portfolio_summary)

    # ==========================================
    # 💎 PROFESSIONAL UI DISPLAY
    # ==========================================
    # 1. Main Data Table
    st.markdown("### 📊 Active Holdings")
    st.dataframe(
        final_df.style.format({
            "Avg Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Total Invested": "${:,.2f}",
            "Current Value": "${:,.2f}",
            "P/L ($)": "${:,.2f}",
            "ROI (%)": "{:.2f}%"
        }).applymap(lambda x: 'color: #00ffcc;' if x > 0 else 'color: #ff4b4b;', subset=['P/L ($)', 'ROI (%)']),
        use_container_width=True,
        hide_index=True
    )

    # 2. Executive Metrics
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    
    total_port_value = final_df["Current Value"].sum()
    total_port_invested = final_df["Total Invested"].sum()
    total_port_profit = total_port_value - total_port_invested
    
    m1.metric("Total Portfolio Value", f"${total_port_value:,.2f}")
    m2.metric("Net Investment", f"${total_port_invested:,.2f}")
    m3.metric("Total Profit/Loss", f"${total_port_profit:,.2f}", 
              delta=f"{(total_port_profit/total_port_invested*100):.2f}%" if total_port_invested != 0 else "0%")

    # 3. Visual Analytics
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_pie = px.pie(final_df, values='Current Value', names='Asset', 
                         title='Portfolio Allocation', hole=0.5, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        fig_bar = px.bar(final_df, x='Asset', y='P/L ($)', color='P/L ($)',
                         title='Profit/Loss per Asset', template="plotly_dark",
                         color_continuous_scale=['#ff4b4b', '#00ffcc'])
        st.plotly_chart(fig_bar, use_container_width=True)
