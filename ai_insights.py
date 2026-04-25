def generate_insights(df, risk_df, corr):

    insights = []

    # 🔹 Trend
    for coin in df["Crypto"].unique():
        coin_df = df[df["Crypto"] == coin]
        change = (coin_df["Close"].iloc[-1] - coin_df["Close"].iloc[0]) / coin_df["Close"].iloc[0]

        if change > 0.05:
            insights.append(f"📈 {coin} shows an upward trend.")
        elif change < -0.05:
            insights.append(f"📉 {coin} shows a downward trend.")

    # 🔹 Risk
    high_risk = risk_df[risk_df["Risk"] == "High"]
    if not high_risk.empty:
        coins = ", ".join(high_risk["Crypto"].tolist())
        insights.append(f"⚠ High risk detected in: {coins}")

    # 🔹 Correlation
    if corr.values.mean() > 0.6:
        insights.append("🔗 Portfolio has high correlation (low diversification).")

    return insights
