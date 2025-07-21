# tools/predict_price.py
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import load_model
import joblib
import os
import json
import logging

# --- CONFIGURATION ---
MODELS_DIR = "models"
MODEL_NAME = "lstm_stock_predictor.keras"
SCALER_NAME = "scaler.pkl"
METADATA_NAME = "model_metadata.json"

logger = logging.getLogger(__name__)

# --- LOAD MODEL AND ARTIFACTS ---
try:
    MODEL_PATH = os.path.join(MODELS_DIR, MODEL_NAME)
    SCALER_PATH = os.path.join(MODELS_DIR, SCALER_NAME)
    METADATA_PATH = os.path.join(MODELS_DIR, METADATA_NAME)

    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    
    LOOKBACK = metadata['lookback']
    N_STEPS_AHEAD = metadata['n_steps_ahead']
    FEATURES_LIST = metadata['features_list']
    CLOSE_COLUMN_INDEX = metadata['close_column_index']
    
    logger.info("Loaded LSTM model and artifacts successfully.")
except Exception as e:
    logger.error(f"Failed to load model or artifacts: {e}", exc_info=True)
    model = None

def calculate_technical_indicators(df):
    # This function must be identical to the one in train_model.py
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
    return df_calc

def predict_stock_price(symbol: str):
    if model is None:
        return {"error": "Model not loaded. Please train the model first by running train_model.py"}

    period_to_fetch = f"{LOOKBACK + 60}d"
    df_original = yf.download(symbol, period=period_to_fetch, interval="1d")
    
    # *** FIX: FLATTEN MULTI-LEVEL COLUMNS ***
    if isinstance(df_original.columns, pd.MultiIndex):
        df_original.columns = df_original.columns.droplevel(1)

    if df_original.empty or len(df_original) < LOOKBACK:
        return {"error": f"Not enough historical data for '{symbol}' to make a prediction."}

    df_with_indicators = calculate_technical_indicators(df_original)
    df_features = df_with_indicators[FEATURES_LIST].dropna()

    if len(df_features) < LOOKBACK:
        return {"error": f"Insufficient data for '{symbol}' after feature engineering. Need at least {LOOKBACK} days."}

    last_sequence_raw = df_features.tail(LOOKBACK)
    scaled_sequence = scaler.transform(last_sequence_raw)
    X_pred = np.reshape(scaled_sequence, (1, LOOKBACK, len(FEATURES_LIST)))
    
    predicted_scaled_prices = model.predict(X_pred)[0]

    dummy_array = np.zeros((len(predicted_scaled_prices), len(FEATURES_LIST)))
    dummy_array[:, CLOSE_COLUMN_INDEX] = predicted_scaled_prices
    inversed_prices = scaler.inverse_transform(dummy_array)[:, CLOSE_COLUMN_INDEX]
    
    current_price = df_original['Close'].iloc[-1]
    
    predictions = {f"Day +{i+1}": round(float(price), 2) for i, price in enumerate(inversed_prices)}

    return {
        "symbol": symbol.upper(),
        "current_price": round(float(current_price), 2),
        "predictions": predictions,
        "note": f"LSTM forecast for the next {N_STEPS_AHEAD} trading days. Not financial advice."
    }