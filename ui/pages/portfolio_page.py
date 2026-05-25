import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, get_holdings

def render_portfolio(df):
    st.markdown('<div class="section-title">💼 Professional Portfolio Manager</div>', unsafe_allow_html=True)

    email = st.session_state.get("email")
    if not email:
        st.warning("Please log in to view your portfolio.")
        return

    # ==========================================
    # 🛒 TRANSACTION INTERFACE
    # ==========================================
    with st.expander("➕ Add New Investment", expanded=True):
        col1, col2, col3 = st.columns(3)
        coin = col1.selectbox("Crypto", sorted(df["Crypto"].unique()))
        amount = col2.number_input("Amount Invested ($)", min_value=0.0, step=10.0)
        date = col3.date_input("Date of Purchase")

        if st.button("Confirm Investment", use_container_width=True):
            if amount > 0:
                add_holding(email, coin, amount, str(date))
                st.success(f"Successfully added ${amount} of {coin}!")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")

    # ==========================================
    # 📊 DATA RETRIEVAL & PROCESSING
    # ==========================================
    data = get_holdings(email)

    if not data:
        st.info("Your portfolio is currently empty. Add an investment above to get started.")
        return

    # Load transactions from DB
    raw_tx_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    raw_tx_df["Date"] = pd.to_datetime(raw_tx_df["Date"])

    # Group transactions to calculate metrics per Coin
    summary_data = []

    for coin_name in raw_tx_df["Crypto"].unique():
        coin_tx = raw_tx_df[raw_tx_df["Crypto"] == coin_name]
        
        total_qty = 0
        total_invested = coin_tx["Amount"].sum()
        
        # Calculate Quantity based on historical price at time of purchase
        for _, row in coin_tx.iterrows():
            coin_history = df[df["Crypto"] == coin_name]
            # Find the closest price on or before the purchase date
            past_data = coin_history[pd.to_datetime(coin_history["Date"]) <= row["Date"]]
            
            if not past_data.empty:
                buy_price = past_data.iloc[-1]["Close"]
                total_qty += row["Amount"] / buy_price
            else:
                # Fallback to earliest available price if date is before dataset range
                buy_price = coin_history.iloc[0]["Close"]
                total_qty += row["Amount"] / buy_price

        # Get latest market price
        current_price = df[df["Crypto"] == coin_name].iloc[-1]["Close"]
        current_value = total_qty * current_price
        avg_buy_price = total_invested / total_qty if total_qty > 0 else 0
        profit_usd = current_value - total_invested
        profit_pct = (profit_usd / total_invested) * 100 if total_invested > 0 else 0

        summary_data.append({
            "Crypto": coin_name,
            "Quantity": total_qty,
            "Avg. Buy Price": avg_buy_price,
            "Current Price": current_price,
            "Invested ($)": total_invested,
            "Current Value ($)": current_value,
            "Profit ($)": profit_usd,
            "Profit (%)": profit_pct
        })

    portfolio_df = pd.DataFrame(summary_data)

    # ==========================================
    # 💎 DISPLAY TABLE
    # ==========================================
    st.markdown("### 📋 Your Holdings")
    
    # Formatting for professional look
    st.dataframe(
        portfolio_df.style.format({
            "Quantity": "{:.6f}",
            "Avg. Buy Price": "${:,.2f}",
            "Current Price": "${:,.2f}",
            "Invested ($)": "${:,.2f}",
            "Current Value ($)": "${:,.2f}",
            "Profit ($)": "${:,.2f}",
            "Profit (%)": "{:.2f}%"
        }).applymap(lambda x: 'color: #00ffcc;' if x > 0 else 'color: #ff4b4b;', subset=['Profit ($)', 'Profit (%)']),
        use_container_width=True,
        hide_index=True
    )

    # ==========================================
    # 📈 TOTAL PORTFOLIO METRICS
    # ==========================================
    total_inv = portfolio_df["Invested ($)"].sum()
    total_val = portfolio_df["Current Value ($)"].sum()
    total_prof = total_val - total_inv
    total_pct = (total_prof / total_inv) * 100 if total_inv > 0 else 0

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Invested", f"${total_inv:,.2f}")
    m2.metric("Current Portfolio Value", f"${total_val:,.2f}")
    m3.metric("Net Profit/Loss", f"${total_prof:,.2f}", delta=f"{total_pct:.2f}%")

    # ==========================================
    # 📊 VISUAL INSIGHTS
    # ==========================================
    st.markdown("### 📊 Portfolio Analytics")
    col_a, col_b = st.columns(2)

    with col_a:
        fig_pie = px.pie(
            portfolio_df,
            names="Crypto",
            values="Current Value ($)",
            title="Asset Allocation",
            hole=0.4,
            template="plotly_dark"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        fig_bar = px.bar(
            portfolio_df,
            x="Crypto",
            y="Profit ($)",
            color="Profit ($)",
            title="Profit/Loss per Asset",
            color_continuous_scale="RdYlGn",
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
