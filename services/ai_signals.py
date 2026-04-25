import pandas as pd


def generate_signals(df: pd.DataFrame):

    df = df.copy()
    df["Return"] = df.groupby("Crypto")["Close"].pct_change()

    signals = []

    for coin in df["Crypto"].unique():

        coin_df = df[df["Crypto"] == coin]

        momentum = coin_df["Return"].tail(5).mean()
        volatility = coin_df["Return"].std()

        if pd.isna(momentum) or pd.isna(volatility):
            continue

        if momentum > 0.01 and volatility < 0.05:
            signal = "BUY 🟢"
        elif momentum < -0.01:
            signal = "SELL 🔴"
        else:
            signal = "HOLD 🟡"

        signals.append({
            "Crypto": coin,
            "Momentum": round(momentum, 4),
            "Volatility": round(volatility, 4),
            "Signal": signal
        })

    return pd.DataFrame(signals)
