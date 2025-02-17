import yfinance as yf
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import math


def get_data(ticker, period='5y', interval='1d'):
    """
    Lädt historische Kursdaten für einen gegebenen Ticker herunter und berechnet die tägliche prozentuale Veränderung.
    """
    df = yf.download(ticker, period=period, interval=interval)
    df['Return'] = df['Close'].pct_change()
    df.dropna(inplace=True)
    return df


def prepare_multi_data(tickers, look_back=60, period='5y', interval='1d'):
    """
    Lädt Daten für mehrere Ticker, kombiniert die Returns, passt einen globalen MinMaxScaler an und erstellt
    Sequenzen für das Training. Zudem werden für jeden Ticker die letzten Sequenzen und der letzte Schlusskurs gespeichert.
    """
    all_returns = []
    data_dict = {}
    for ticker in tickers:
        data = get_data(ticker, period, interval)
        data_dict[ticker] = data
        returns = data['Return'].values.reshape(-1, 1)
        all_returns.append(returns)

    all_returns = np.vstack(all_returns)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(all_returns)

    all_sequences = []
    all_labels = []
    last_seqs = {}
    last_closes = {}

    for ticker in tickers:
        data = data_dict[ticker]
        returns = data['Return'].values.reshape(-1, 1)
        scaled_returns = scaler.transform(returns)

        sequences = []
        labels = []
        for i in range(look_back, len(scaled_returns)):
            sequences.append(scaled_returns[i - look_back:i, 0])
            labels.append(scaled_returns[i, 0])
        sequences = np.array(sequences)
        labels = np.array(labels)

        last_seq = scaled_returns[-look_back:]
        last_seq = np.reshape(last_seq, (1, look_back, 1))
        last_seqs[ticker] = last_seq
        last_closes[ticker] = float(data['Close'].iloc[-1])

        sequences = np.reshape(sequences, (sequences.shape[0], sequences.shape[1], 1))
        all_sequences.append(sequences)
        all_labels.append(labels)

    X = np.vstack(all_sequences)
    y = np.hstack(all_labels)
    return X, y, scaler, last_seqs, last_closes


def build_model(input_shape):
    """
    Erstellt ein LSTM-Modell zur Vorhersage von Kursveränderungen.
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_and_predict(tickers, look_back=60, period='5y', interval='1d'):
    """
    Lädt und kombiniert Daten mehrerer Ticker, trainiert ein globales Modell und prognostiziert
    für jeden Ticker den nächsten Schlusskurs.
    """
    print(f"\nVerarbeite Ticker: {', '.join(tickers)}")
    X, y, scaler, last_seqs, last_closes = prepare_multi_data(tickers, look_back, period, interval)

    train_size = int(len(X) * 0.8)
    x_train, y_train = X[:train_size], y[:train_size]
    x_test, y_test = X[train_size:], y[train_size:]

    model = build_model((x_train.shape[1], 1))
    model.summary()

    history = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=1)  # Kein EarlyStopping

    y_pred_test = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred_test)
    rmse = math.sqrt(mse)
    r2 = r2_score(y_test, y_pred_test)

    print("\nModellbewertung (globaler Datensatz):")
    print(f"Test MSE:   {mse:.6f}")
    print(f"Test RMSE:  {rmse:.6f}")
    print(f"Test R²:    {r2:.6f}")

    predictions = {}
    for ticker in tickers:
        last_sequence = last_seqs[ticker]
        predicted_scaled = model.predict(last_sequence)
        predicted_return = scaler.inverse_transform(predicted_scaled)[0, 0]
        last_close = last_closes[ticker]
        predicted_price = last_close * (1 + predicted_return)
        predictions[ticker] = (float(predicted_price), float(predicted_return * 100))

    return predictions


tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

predictions = train_and_predict(tickers, look_back=30)

print("\nVorhersagen für den nächsten Tag:")
for ticker, (price, change) in predictions.items():
    print(f"{ticker}: {price:.2f} USD ({change:.2f}%)")
