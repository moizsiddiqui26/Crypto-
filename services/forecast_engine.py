import pandas as pd
from services.lstm_model import predict_future


def get_forecast_summary(df: pd.DataFrame, investment: float, days: int = 7):

    if df.empty:
        return None

    series = df["Close"].values

    preds = predict_future(series, days)

    if len(preds) == 0:
        return None

    current_price = series[-1]
    predicted_price = preds[-1]

    units = investment / current_price
    expected_value = units * predicted_price

    profit_pct = ((predicted_price - current_price) / current_price) * 100

    return {
        "future_prices": preds,
        "current_price": current_price,
        "predicted_price": predicted_price,
        "expected_value": expected_value,
        "profit_pct": profit_pct
    }
