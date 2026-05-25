import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys

# --- PATH RESOLUTION (FOR STREAMLIT CLOUD) ---
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from db.models import add_holding, get_holdings, sell_holding
except ImportError:
    st.error("Error: Could not load database models.")

def render_portfolio(df):
    st.markdown('<div class="section-title">👤 Professional Portfolio Manager</div>', unsafe_allow_html=True)
    
    email = st.session_state.get("email")
    if not email:
        st.warning("Please log in to view your portfolio.")
        return

    # ==========================================
    # 📊 1. PORTFOLIO ANALYTICS (NOW AT TOP)
    # ==========================================
    data = get_holdings(email)

    if not data:
        st.info("Your portfolio is currently empty. Scroll down to add your first transaction!")
    else:
        # Convert DB data to DataFrame
        portfolio_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
        portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

        # Calculate Current Prices from provided historical data
        latest_prices = df.groupby("Crypto").last().reset_index()[["Crypto", "Close"]]
        latest_prices.rename(columns={"Close": "Current Price"}, inplace=True)
        portfolio_df = portfolio_df.merge(latest_prices, on="Crypto", how="left")

        # Calculate Buy Price based on transaction date
        def get_buy_price(row):
            coin_df = df[df["Crypto"] == row["Crypto"]]
            past_data = coin_df[coin_df["Date"] <= row["Date"]]
            return past_data.iloc[-1]["Close"] if not past_data.empty else np.nan

        portfolio_df["Buy Price"] = portfolio_df.apply(get_buy_price, axis=1)
        
        # Calculate Holdings and Value
        portfolio_df["Quantity"] = portfolio_df["Amount"] / portfolio_df["Buy Price"]
        portfolio_df["Current Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]
        portfolio_df["Profit ($)"] = portfolio_df["Current Value"] - portfolio_df["Amount"]
        
        # --- Summary Metrics ---
        total_invested = portfolio_df["Amount"].sum()
        total_value = portfolio_df["Current Value"].sum()
        total_profit = total_value - total_invested
        profit_pct = (total_profit / total_invested * 100) if total_invested != 0 else 0

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Invested", f"${total_invested:,.2f}")
        m2.metric("Market Value", f"${total_value:,.2f}")
        m3.metric("Net Profit", f"${total_profit:,.2f}", delta=f"{profit_pct:.2f}%")

        # --- Holdings Table ---
        st.markdown("### 📋 Current Holdings")
        st.dataframe(
            portfolio_df[["Crypto", "Quantity", "Buy Price", "Current Price", "Current Value", "Profit ($)"]].style.format({
                "Quantity": "{:.6f}",
                "Buy Price": "${:,.2f}",
                "Current Price": "${:,.2f}",
                "Current Value": "${:,.2f}",
                "Profit ($)": "${:,.2f}"
            }).map(lambda x: 'color: #00ffcc;' if x > 0 else 'color: #ff4b4b;', subset=['Profit ($)']),
            use_container_width=True, hide_index=True
        )

        # --- Visual Charts ---
        st.markdown("### 📊 Allocation & Performance")
        c1, c2 = st.columns(2)
        
        with c1:
            fig1 = px.pie(portfolio_df, names="Crypto", values="Current Value", 
                          title="Asset Allocation", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            fig2 = px.bar(portfolio_df, x="Crypto", y="Profit ($)", color="Profit ($)",
                          color_continuous_scale=["#ff4b4b", "#00ffcc"], title="Profit/Loss by Asset",
                          template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

    # ==========================================
    # 🛒 2. TRANSACTION INTERFACE (NOW AT BOTTOM)
    # ==========================================
    st.markdown("---")
    st.markdown("### ➕ / ➖ Execute Transaction")
    
    with st.container(border=True):
        t_col1, t_col2, t_col3, t_col4 = st.columns([1, 2, 2, 2])
        
        action = t_col1.radio("Action", ["Buy", "Sell"])
        coin_list = sorted(df["Crypto"].unique())
        coin = t_col2.selectbox("Select Asset", coin_list)
        cash_amount = t_col3.number_input("Amount ($)", min_value=0.0, step=100.0)
        tx_date = t_col4.date_input("Transaction Date")

        if st.button("Confirm Order", use_container_width=True):
            if cash_amount <= 0:
                st.error("Please enter a valid amount.")
            else:
                if action == "Buy":
                    add_holding(email, coin, cash_amount, str(tx_date))
                    st.success(f"Successfully bought ${cash_amount:,.2f} of {coin}!")
                else:
                    # Basic Sell validation
                    current_bal = portfolio_df[portfolio_df["Crypto"] == coin]["Amount"].sum() if not data == [] else 0
                    if cash_amount > current_bal:
                        st.error(f"Insufficient funds! You only have ${current_bal:,.2f} available.")
                    else:
                        sell_holding(email, coin, cash_amount, str(tx_date))
                        st.warning(f"Sold ${cash_amount:,.2f} of {coin}!")
                
                st.rerun()

    # ==========================================
    # 📖 USER GUIDE
    # ==========================================
    with st.expander("📖 Portfolio Mastery Guide"):
        st.markdown("""
        - **Quantity:** Calculated automatically based on the coin price on your selected 'Transaction Date'.
        - **Market Value:** Real-time valuation based on the latest available market data.
        - **Profit/Loss:** Shows your absolute gain or loss since the time of purchase.
        """)
