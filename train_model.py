# train_model.py
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib
import os
import json
import time

# --- CONFIGURATION ---
MODELS_DIR = "models"
MODEL_NAME = "lstm_stock_predictor.keras"
SCALER_NAME = "scaler.pkl"
METADATA_NAME = "model_metadata.json"
N_STEPS_AHEAD = 5
LOOKBACK = 60

def get_stock_data(symbol, period="10y", retries=3, delay=5):
    """Fetches stock data and flattens columns if they are a MultiIndex."""
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}/{retries} to download data for {symbol}...")
            data = yf.download(symbol, period=period, interval="1d")
            if not data.empty:
                # *** FIX: FLATTEN MULTI-LEVEL COLUMNS ***
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)
                return data[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    return None

def calculate_technical_indicators(df):
    """Calculates technical indicators and ensures the DataFrame is clean."""
    df_calc = df.copy()
    df_calc['SMA_10'] = df_calc['Close'].rolling(window=10).mean()
    df_calc['SMA_20'] = df_calc['Close'].rolling(window=20).mean()
    df_calc['EMA_10'] = df_calc['Close'].ewm(span=10, adjust=False).mean()
    df_calc['EMA_20'] = df_calc['Close'].ewm(span=20, adjust=False).mean()
    
    delta = df_calc['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    with np.errstate(divide='ignore', invalid='ignore'):
        rs = gain / loss
        df_calc['RSI'] = 100 - (100 / (1 + rs))
    df_calc['RSI'].fillna(50, inplace=True)
    
    exp1 = df_calc['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df_calc['Close'].ewm(span=26, adjust=False).mean()
    df_calc['MACD'] = exp1 - exp2
    df_calc['Signal_Line'] = df_calc['MACD'].ewm(span=9, adjust=False).mean()
    df_calc['MACD_Hist'] = df_calc['MACD'] - df_calc['Signal_Line']
    
    df_calc.dropna(inplace=True)
    return df_calc

def prepare_data(df, lookback, n_steps_ahead):
    """Prepares data for LSTM, creating sequences for multi-step prediction."""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)
    
    close_column_index = df.columns.get_loc('Close')
    
    X, y = [], []
    for i in range(lookback, len(scaled_data) - n_steps_ahead + 1):
        X.append(scaled_data[i - lookback:i, :])
        y.append(scaled_data[i:i + n_steps_ahead, close_column_index])

    return np.array(X), np.array(y), scaler

def build_model(input_shape, n_steps_ahead):
    """Builds the LSTM model for multi-step prediction."""
    model = Sequential([
        LSTM(units=100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=100, return_sequences=False),
        Dropout(0.2),
        Dense(units=50),
        Dense(units=n_steps_ahead)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model

def train_and_save_model(symbol="AAPL"):
    print(f"--- Starting model training for {symbol} ---")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    MODEL_PATH = os.path.join(MODELS_DIR, MODEL_NAME)
    SCALER_PATH = os.path.join(MODELS_DIR, SCALER_NAME)
    METADATA_PATH = os.path.join(MODELS_DIR, METADATA_NAME)

    df_original = get_stock_data(symbol)
    if df_original is None or df_original.empty:
        print(f"ERROR: No data found for '{symbol}'. Cannot train model.")
        return

    df_features = calculate_technical_indicators(df_original)

    if len(df_features) < (LOOKBACK + N_STEPS_AHEAD + 50):
        print(f"ERROR: Insufficient data for '{symbol}'. Cannot train model.")
        return

    features_list = df_features.columns.tolist()
    close_column_index = df_features.columns.get_loc('Close')

    X, y, scaler = prepare_data(df_features, LOOKBACK, N_STEPS_AHEAD)
    
    if len(X) == 0:
        print("ERROR: Not enough data to create training sequences.")
        return
        
    model = build_model((X.shape[1], X.shape[2]), N_STEPS_AHEAD)
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

    print(f"Training model with {len(X)} samples...")
    model.fit(X, y,
              epochs=100,
              batch_size=32,
              validation_split=0.1,
              callbacks=[early_stopping, reduce_lr],
              verbose=1)

    print("--- Model training complete ---")

    model.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    model_metadata = {
        'lookback': LOOKBACK,
        'n_steps_ahead': N_STEPS_AHEAD,
        'features_list': features_list,
        'close_column_index': int(close_column_index)
    }
    with open(METADATA_PATH, 'w') as f:
        json.dump(model_metadata, f, indent=4)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Scaler saved to: {SCALER_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")

if __name__ == "__main__":
    train_and_save_model(symbol="AAPL")