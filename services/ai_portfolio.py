import pandas as pd
import numpy as np


def prepare_metrics(df: pd.DataFrame):

    df = df.copy()
    df["Return"] = df.groupby("Crypto")["Close"].pct_change()

    vol = df.groupby("Crypto")["Return"].std().reset_index(name="Volatility")

    total_return = df.groupby("Crypto").apply(
        lambda x: (x.Close.iloc[-1] - x.Close.iloc[0]) / x.Close.iloc[0]
    ).reset_index(name="Total Return")

    metrics = total_return.merge(vol, on="Crypto")

    return metrics


def optimize_portfolio(df: pd.DataFrame, investment: float):

    metrics = prepare_metrics(df)

    if metrics.empty:
        return pd.DataFrame()

    # Sharpe-like score
    metrics["Score"] = metrics["Total Return"] / (metrics["Volatility"] + 1e-6)

    metrics = metrics.replace([np.inf, -np.inf], np.nan).dropna()
    metrics = metrics[metrics["Score"] > 0]

    if metrics.empty:
        return pd.DataFrame()

    metrics["Allocation %"] = metrics["Score"] / metrics["Score"].sum() * 100
    metrics["Investment"] = (metrics["Allocation %"] / 100) * investment

    return metrics.sort_values("Allocation %", ascending=False).round(2)
