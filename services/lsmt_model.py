import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler


def prepare_data(series, window=10):

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(series.reshape(-1, 1))

    X, y = [], []

    for i in range(window, len(scaled)):
        X.append(scaled[i-window:i])
        y.append(scaled[i])

    return np.array(X), np.array(y), scaler


def train_model(series):

    X, y, scaler = prepare_data(series)

    if len(X) == 0:
        return None, None

    model = Sequential([
        LSTM(50, input_shape=(X.shape[1], 1)),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=5, batch_size=8, verbose=0)

    return model, scaler


def predict_future(series, days=5):

    if len(series) < 20:
        return []

    model, scaler = train_model(series)

    if model is None:
        return []

    window = 10
    last_window = series[-window:]
    last_window = scaler.transform(last_window.reshape(-1, 1))

    preds = []

    for _ in range(days):
        pred = model.predict(last_window.reshape(1, window, 1), verbose=0)
        preds.append(pred[0][0])
        last_window = np.append(last_window[1:], pred, axis=0)

    preds = scaler.inverse_transform(np.array(preds).reshape(-1, 1))
    return preds.flatten()
