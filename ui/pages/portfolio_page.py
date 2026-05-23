import streamlit as st
import pandas as pd
import plotly.express as px
from db.models import add_holding, get_holdings

def render_portfolio(df):
    st.markdown('<div class="section-title">👤 Portfolio</div>', unsafe_allow_html=True)

    email = st.session_state.get("email")

    col1, col2, col3 = st.columns(3)
    coin = col1.selectbox("Crypto", df["Crypto"].unique())
    amount = col2.number_input("Amount ($)", min_value=0.0)
    date = col3.date_input("Date")

    if st.button("Add Investment"):
        add_holding(email, coin, amount, str(date))
        st.success("Added!")

    st.markdown("<br>", unsafe_allow_html=True)

    data = get_holdings(email)

    if not data:
        st.info("No investments yet")
        return

    portfolio_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

    # =========================
    # 🔥 CALCULATE CURRENT PRICE
    # =========================
    latest_prices = df.groupby("Crypto").last().reset_index()[["Crypto", "Close"]]
    latest_prices.rename(columns={"Close": "Current Price"}, inplace=True)

    # Merge with portfolio
    portfolio_df = portfolio_df.merge(latest_prices, on="Crypto", how="left")

    # =========================
    # 🔥 CALCULATE BUY PRICE
    # =========================
    def get_buy_price(row):
        coin_df = df[df["Crypto"] == row["Crypto"]]
        past_data = coin_df[coin_df["Date"] <= row["Date"]]

        if past_data.empty:
            return np.nan

        return past_data.iloc[-1]["Close"]

    portfolio_df["Buy Price"] = portfolio_df.apply(get_buy_price, axis=1)

    # =========================
    # 🔥 CALCULATE PROFIT
    # =========================
    portfolio_df["Quantity"] = portfolio_df["Amount"] / portfolio_df["Buy Price"]

    portfolio_df["Current Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]

    portfolio_df["Profit ($)"] = portfolio_df["Current Value"] - portfolio_df["Amount"]

    portfolio_df["Profit (%)"] = (portfolio_df["Profit ($)"] / portfolio_df["Amount"]) * 100

    # Clean format
    portfolio_df = portfolio_df.round(2)

    # =========================
    # 💎 DISPLAY
    # =========================
    st.dataframe(portfolio_df, use_container_width=True)

    # =========================
    # 📊 TOTAL PORTFOLIO SUMMARY
    # =========================
    total_invested = portfolio_df["Amount"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = total_value - total_invested
    profit_pct = (total_profit / total_invested) * 100 if total_invested > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Invested", f"${total_invested:.2f}")
    col2.metric("Current Value", f"${total_value:.2f}")
    col3.metric("Profit", f"${total_profit:.2f} ({profit_pct:.2f}%)")
    st.markdown("### 📊 Portfolio Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(
        portfolio_df,
        names="Crypto",
        values="Current Value",
        title="Investment Allocation",
        template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True, key="portfolio_pie")

        st.caption("💰 Shows how your investment is distributed across coins.")

    with col2:
        fig2 = px.bar(
            portfolio_df,
            x="Crypto",
            y="Profit ($)",
            color="Profit ($)",
            color_continuous_scale=["red", "green"],
            title="Profit / Loss by Coin",
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True, key="portfolio_profit")

        st.caption("📈 Shows which coins are making profit or loss.")

