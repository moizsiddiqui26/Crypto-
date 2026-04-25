import pandas as pd
import numpy as np


# =========================
# 📈 TREND ANALYSIS
# =========================
def analyze_trend(df: pd.DataFrame):
    insights = []

    if df is None or df.empty:
        return insights

    for coin in df["Crypto"].unique():
        coin_df = df[df["Crypto"] == coin].sort_values("Date")

        if len(coin_df) < 2:
            continue

        start_price = coin_df["Close"].iloc[0]
        end_price = coin_df["Close"].iloc[-1]

        change = (end_price - start_price) / start_price

        if change > 0.05:
            insights.append(f"📈 {coin} is showing a strong upward trend.")
        elif change < -0.05:
            insights.append(f"📉 {coin} is showing a downward trend.")
        else:
            insights.append(f"➖ {coin} is relatively stable.")

    return insights


# =========================
# ⚠️ RISK ANALYSIS
# =========================
def analyze_risk(risk_df: pd.DataFrame):
    insights = []

    if risk_df is None or risk_df.empty:
        return insights

    high = risk_df[risk_df["Risk"] == "High"]
    medium = risk_df[risk_df["Risk"] == "Medium"]

    if not high.empty:
        coins = ", ".join(high["Crypto"].tolist())
        insights.append(f"⚠ High risk detected in: {coins}")

    if not medium.empty:
        coins = ", ".join(medium["Crypto"].tolist())
        insights.append(f"⚡ Moderate risk in: {coins}")

    if high.empty and medium.empty:
        insights.append("✅ All assets are currently low risk.")

    return insights


# =========================
# 🔗 CORRELATION ANALYSIS
# =========================
def analyze_correlation(corr: pd.DataFrame):
    insights = []

    if corr is None or corr.empty:
        return insights

    # Remove self-correlation
    corr_values = corr.values[np.triu_indices_from(corr.values, k=1)]

    if len(corr_values) == 0:
        return insights

    avg_corr = np.nanmean(corr_values)

    if avg_corr > 0.7:
        insights.append("🔗 High correlation detected — portfolio is not well diversified.")
    elif avg_corr > 0.4:
        insights.append("⚖ Moderate correlation — some diversification present.")
    else:
        insights.append("🌐 Low correlation — good diversification.")

    return insights


# =========================
# 📊 VOLATILITY ANALYSIS
# =========================
def analyze_volatility(df: pd.DataFrame):
    insights = []

    if df is None or df.empty:
        return insights

    df = df.copy()
    df["Return"] = df.groupby("Crypto")["Close"].pct_change()

    vol = df.groupby("Crypto")["Return"].std()

    for coin, v in vol.items():
        if pd.isna(v):
            continue

        if v > 0.05:
            insights.append(f"🔥 {coin} is highly volatile.")
        elif v > 0.02:
            insights.append(f"⚡ {coin} shows moderate volatility.")
        else:
            insights.append(f"🟢 {coin} is relatively stable.")

    return insights


# =========================
# 🧠 MAIN FUNCTION
# =========================
def generate_insights(df: pd.DataFrame, risk_df: pd.DataFrame, corr: pd.DataFrame):

    insights = []

    try:
        insights += analyze_trend(df)
        insights += analyze_risk(risk_df)
        insights += analyze_correlation(corr)
        insights += analyze_volatility(df)

    except Exception as e:
        return [f"⚠ Error generating insights: {str(e)}"]

    # Remove duplicates
    insights = list(dict.fromkeys(insights))

    # Limit to top insights
    if len(insights) > 8:
        insights = insights[:8]

    if not insights:
        insights.append("✅ No major signals detected. Market looks stable.")

    return insights
