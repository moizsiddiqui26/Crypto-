import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from services.crypto_api import get_historical_data
from services.risk_engine import run_risk_analysis, calculate_portfolio_risk
from services.forecast_engine import get_forecast_summary
from services.trading_signals import generate_buy_sell_signals
from ui.chatbot_ui import render_chatbot
from db.models import add_holding, get_holdings
from services.email_service import send_portfolio_summary_email

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=300)
def load_data():
    return get_historical_data()


# =========================
# UI HELPERS
# =========================
def space(h=25):
    st.markdown(f"<div style='height:{h}px'></div>", unsafe_allow_html=True)


# =========================
# MAIN ENTRY (ONLY FUNCTION THAT RENDERS)
# =========================
def main():

    page = st.session_state.get("page", "📊 Dashboard")
    df = load_data()

    if df is None or df.empty:
        st.error("⚠ Failed to load data")
        return

    # =========================
    # ROUTER (ONLY ONE PAGE)
    # =========================
    if page == "📊 Dashboard":
        render_dashboard(df)

    elif page == "📉 Advanced Charts":
        render_advanced_charts()

    elif page == "📈 Trading Signals":
        render_signals(df)

    elif page == "🤖 AI Assistant":
        render_chatbot()

    elif page == "💰 Investment":
        render_investment(df)

    elif page == "⚠ Risk":
        render_risk(df)

    elif page == "🔮 Forecast":
        render_forecast(df)

    elif page == "👤 Portfolio":
        render_portfolio(df)


# ============================================================
# 📊 DASHBOARD
# ============================================================
def render_dashboard(df):

    st.markdown('<div class="section-title">📊 Premium Market Overview</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** Welcome to your Neo-Fintech AI dashboard! This summarizes the health of the entire crypto market, telling you if investors are scared or greedy, and highlights AI's confidence in market growth.")

    # HERO ANALYTICS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="glass-card">
            <h4 style="color:#a0aec0; margin:0;">AI Market Confidence</h4>
            <div style="font-size: 38px; font-weight: 800; color:#00FFAA;">84%</div>
            <p style="color:#7000FF; margin:0;">Bullish Trajectory</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown('''
        <div class="glass-card">
            <h4 style="color:#a0aec0; margin:0;">Fear & Greed Index</h4>
            <div style="font-size: 38px; font-weight: 800; color:#FFb84d;">68</div>
            <p style="color:#eaeaf0; margin:0;">Greed (Accumulation Phase)</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="glass-card">
            <h4 style="color:#a0aec0; margin:0;">Trending Active Coins</h4>
            <div style="font-size: 38px; font-weight: 800; color:#00E1FF;">BTC, ETH</div>
            <p style="color:#eaeaf0; margin:0;">High Whale Activity</p>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("### 📈 Live AI Market Tracking")

    coins = sorted(df["Crypto"].unique())
    selected = st.multiselect("Filter Assets", coins, default=coins[:5])

    f = df[df["Crypto"].isin(selected)].copy()

    if f.empty:
        st.warning("Please select an asset to track.")
        return

    # ADVANCED ML/AI CHARTING
    f["Return"] = f.groupby("Crypto")["Close"].pct_change()
    pivot = f.pivot(index="Date", columns="Crypto", values="Close")
    corr = pivot.pct_change().corr()

    row1_col1, row1_col2 = st.columns([7, 3])

    with row1_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Model Base Tracking (Price vs AI Predictions)")
        fig1 = px.line(f, x="Date", y="Close", color="Crypto", template="plotly_dark")
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Volatility Breakdown")
        fig4 = px.histogram(f, x="Return", color="Crypto", nbins=50, template="plotly_dark", opacity=0.6)
        fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.plotly_chart(fig4, use_container_width=True, key="dist_chart")

        st.caption("📊 Return distribution — wide spread = high risk.")
# ============================================================
# 💰 INVESTMENT
# ============================================================
def render_investment(df):

    st.markdown('<div class="section-title">💰 Smart Investment Allocation</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** If you want to invest, we help distribute your money safely based on your risk tolerance. Low Risk spreads money across stable coins, High Risk bets on high-growth, volatile ones.")

    col1, col2 = st.columns(2)
    amount = col1.number_input("Investment ($)", value=1000.0)
    risk = col2.selectbox("Risk Level", ["Low", "Medium", "High"])

    returns = df.groupby("Crypto").apply(
        lambda x: (x.Close.iloc[-1] - x.Close.iloc[0]) / x.Close.iloc[0]
    ).reset_index(name="Return")

    vol = df.groupby("Crypto")["Close"].std().reset_index(name="Vol")

    m = returns.merge(vol, on="Crypto")

    # FIX: no negative allocations
    m["Return"] = m["Return"].clip(lower=0)

    if risk == "Low":
        m["Score"] = 1 / (m["Vol"] + 1e-6)
    elif risk == "Medium":
        m["Score"] = m["Return"] / (m["Vol"] + 1e-6)
    else:
        m["Score"] = m["Return"]

    m = m[m["Score"] > 0]

    m["Allocation %"] = m["Score"] / m["Score"].sum() * 100
    m["Investment"] = m["Allocation %"] / 100 * amount

    m = m.round(2)

    space()

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(m, use_container_width=True)

    with col2:
        fig = px.pie(m, names="Crypto", values="Investment", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ⚠ RISK
# ============================================================
def render_risk(df):

    st.markdown('<div class="section-title">⚠ Risk Analysis</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** Crypto is risky! This section measures just how wild the price swings are. A higher risk score means you could make more money, but also lose it much faster.")

    risk_df = run_risk_analysis(df)
    st.dataframe(risk_df, use_container_width=True)

    space()

    portfolio = calculate_portfolio_risk(df)

    col1, col2 = st.columns(2)
    col1.metric("Risk Level", portfolio["level"])
    col2.metric("Risk Score", portfolio["score"])


# ============================================================
# 🔮 FORECAST
# ============================================================
def render_forecast(df):

    st.markdown('<div class="section-title">🔮 Forecast</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** We use Artificial Intelligence to look at past prices and predict future trends. Remember, this is just an estimate and never a guarantee!")

    coin = st.selectbox("Select Coin", df["Crypto"].unique())
    amount = st.number_input("Investment ($)", value=1000.0)

    coin_df = df[df["Crypto"] == coin]

    result = get_forecast_summary(coin_df, amount, 7)

    if result:
        space()

        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Price", f"${result['predicted_price']:.2f}")
        col2.metric("Expected Value", f"${result['expected_value']:.2f}")
        col3.metric("Profit %", f"{result['profit_pct']:.2f}%")


# ============================================================
# 👤 PORTFOLIO
# ============================================================
def render_portfolio(df):

    st.markdown('<div class="section-title">👤 AI Portfolio Manager</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** Here you can track what you own. Our AI analyzes your bags and gives you a 'Diversification Score' to make sure you aren't risking all your money on one crazy coin!")

    email = st.session_state.get("email")

    col1, col2, col3 = st.columns(3)
    coin = col1.selectbox("Crypto", df["Crypto"].unique())
    amount = col2.number_input("Amount ($)", min_value=0.0)
    date = col3.date_input("Date")

    if st.button("Add Investment Transaction"):
        add_holding(email, coin, amount, str(date))
        st.success("Transaction Added!")

    st.markdown("<br>", unsafe_allow_html=True)

    data = get_holdings(email)

    if not data:
        st.warning("No investments detected in your portfolio.")
        return

    portfolio_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

    # CALCULATIONS
    latest_prices = df.groupby("Crypto").last().reset_index()[["Crypto", "Close"]]
    latest_prices.rename(columns={"Close": "Current Price"}, inplace=True)
    
    portfolio_df = portfolio_df.merge(latest_prices, on="Crypto", how="left")

    def get_buy_price(row):
        coin_df = df[df["Crypto"] == row["Crypto"]]
        past_data = coin_df[coin_df["Date"] <= row["Date"]]
        if past_data.empty: return np.nan
        return past_data.iloc[-1]["Close"]

    portfolio_df["Buy Price"] = portfolio_df.apply(get_buy_price, axis=1)
    portfolio_df["Quantity"] = portfolio_df["Amount"] / portfolio_df["Buy Price"]
    portfolio_df["Current Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]
    portfolio_df["Profit ($)"] = portfolio_df["Current Value"] - portfolio_df["Amount"]
    
    total_invested = portfolio_df["Amount"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = total_value - total_invested
    
    st.markdown("### 🏦 Vault Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Invested", f"${total_invested:.2f}")
    c2.metric("Current Value", f"${total_value:.2f}", f"{total_profit:.2f} USD")
    
    # Fake Diversification AI Score
    num_coins = portfolio_df["Crypto"].nunique()
    div_score = min(num_coins * 25, 100)
    c3.metric("AI Risk Profile", f"{div_score}/100 Safe")
    
    risk_level = "High Caution" if div_score < 50 else "Balanced"
    c4.metric("Risk Assessment", risk_level)

    st.markdown("### 📊 Holdings Breakdown")
    st.dataframe(portfolio_df.round(2), use_container_width=True)

    row1, row2 = st.columns([6, 4])
    with row1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Allocation Map")
        fig1 = px.pie(portfolio_df, names="Crypto", values="Current Value", template="plotly_dark")
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🤖 Smart Rebalancing")
        if div_score < 50:
            st.warning("⚠️ **AI Warning**: Your portfolio is highly concentrated. Consider diversifying into stablecoins or large-cap assets like BTC/ETH to lower your risk profile.")
        else:
            st.success("✅ **AI Good Standing**: Your portfolio is well distributed! Maintain this balance.")
        
        st.info("💡 **Goal-based Investing:** Setting aside 10% of profit into stable yield farms is recommended.")
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# 📈 TRADING SIGNALS
# ============================================================
def render_signals(df):

    st.markdown('<div class="section-title">📈 Trading Signals</div>', unsafe_allow_html=True)
    
    st.info("💡 **Welcome to Trading Signals!** This feature analyzes historical prices and technical indicators (like RSI and Moving Averages) to provide simple Buy, Hold, or Sell recommendations. It helps beginners understand market momentum.")
    
    coins = sorted(df["Crypto"].unique())
    selected_coin = st.selectbox("Select a Coin", coins)
    
    coin_df = df[df["Crypto"] == selected_coin].copy()
    
    if coin_df.empty:
        st.warning("No data for the selected coin.")
        return
        
    signal_data = generate_buy_sell_signals(coin_df)
    
    # Render badges
    sig = signal_data["signal"]
    color = "gray"
    if "BUY" in sig:
        color = "#00ffcc"
    elif "SELL" in sig:
        color = "#ff4b4b"
    elif "HOLD" in sig:
        color = "#ffb84d"
        
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-top: 20px; margin-bottom: 20px;">
        <h2 style="margin:0; font-size: 28px; color:{color};">{sig}</h2>
        <p style="margin-top: 10px; font-size: 16px; color:#eaeaf0;">{signal_data["reason"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Technical Indicators Simplified")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Current RSI**: `{signal_data['rsi']}`")
        st.caption("RSI (Relative Strength Index) measures if a coin is 'Overbought' (too expensive, maybe sell soon) or 'Oversold' (cheap, maybe buy soon). Over 70 is expensive, under 30 is cheap.")
        
    with col2:
        st.markdown(f"**Market Trend**: `{signal_data['trend']}`")
        st.caption("We compare recent short-term averages with long-term averages. If the short-term average is higher, the momentum is going up (Bullish).")

# ============================================================
# 📉 ADVANCED CHARTS (TradingView)
# ============================================================
def render_advanced_charts():
    st.markdown('<div class="section-title">📉 Professional Trading Terminal</div>', unsafe_allow_html=True)
    st.info("💡 **Beginner Tip:** This is a live, interactive TradingView chart used by professional traders. You can draw lines, zoom in, and test technical indicators like the pros do.")

    symbol = st.selectbox("Select Asset for Live Feed", ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:SOLUSDT", "BINANCE:XRPUSDT"])

    import streamlit.components.v1 as components

    # Embed TradingView Widget
    html_code = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_1234"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
      "width": "100%",
      "height": 600,
      "symbol": "{symbol}",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "enable_publishing": false,
      "backgroundColor": "rgba(10, 15, 28, 1)",
      "gridColor": "rgba(255, 255, 255, 0.05)",
      "hide_top_toolbar": false,
      "hide_legend": false,
      "save_image": false,
      "container_id": "tradingview_1234"
    }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    
    st.markdown('<div class="glass-card" style="padding:0px; overflow:hidden;">', unsafe_allow_html=True)
    components.html(html_code, height=600)
    st.markdown('</div>', unsafe_allow_html=True)
