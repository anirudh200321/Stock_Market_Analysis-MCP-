import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np # For handling potential NaN values

from tools.fetch_price import get_current_price # Still useful for current price check

def predict_price(symbol: str):
    """
    Predicts the next-day stock price for a given symbol using a simple linear regression model.
    The model is trained on recent historical closing prices.
    This is a simplified ML model and NOT for financial advice.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "GOOGL").

    Returns:
        dict: A dictionary containing the symbol, current price, predicted price,
              and a note about the prediction method, or an error message if
              data cannot be retrieved or prediction fails.
    """
    try:
        # Fetch current price for context
        current_data = get_current_price(symbol)
        if "error" in current_data:
            return {"error": f"Could not predict price for '{symbol}': {current_data['error']}"}
        current_price = current_data["price"]

        # Fetch historical data for model training (e.g., last 60 days)
        # We need enough data to create lagged features
        stock = yf.Ticker(symbol)
        hist = stock.history(period="60d") # Fetch 60 days of data

        if hist.empty or len(hist) < 10: # Need at least some data points for features
            return {"error": f"Insufficient historical data found for '{symbol}' to train model."}

        # Prepare data for linear regression
        # We'll use the last 5 days' closing prices to predict the next day's price
        df = pd.DataFrame(hist['Close'])
        
        # Create lagged features
        for i in range(1, 6): # Lag features: Close price from 1 to 5 days ago
            df[f'Close_Lag_{i}'] = df['Close'].shift(i)
        
        # Drop rows with NaN values (due to shifting)
        df.dropna(inplace=True)

        if df.empty:
            return {"error": f"Not enough valid data after feature engineering for '{symbol}' to train model."}

        # Define features (X) and target (y)
        # X will be the lagged closing prices, y will be the current closing price (which we want to predict for the 'next' day)
        features = [f'Close_Lag_{i}' for i in range(1, 6)]
        X = df[features]
        y = df['Close'] # The target is the 'current' close price for training

        # Ensure X and y have enough samples
        if len(X) < 2: # Need at least 2 samples to train a linear model
            return {"error": f"Not enough data points ({len(X)}) for '{symbol}' to train the ML model."}

        # Train the Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the next day's price
        # Use the most recent 'lagged' features available in the original historical data
        # The last row of hist (before dropping NaNs) contains the most recent 5 days needed for prediction
        last_known_prices = hist['Close'].iloc[-5:].values.reshape(1, -1) # Get last 5 closing prices

        # Ensure last_known_prices has 5 values
        if len(last_known_prices[0]) != 5:
            return {"error": f"Could not get enough recent historical data for '{symbol}' to make a prediction."}

        predicted_price = model.predict(last_known_prices)[0]
        predicted_price = round(predicted_price, 2)

        return {
            "symbol": symbol.upper(),
            "current_price": current_price,
            "predicted_price": predicted_price,
            "note": "This prediction uses a simple linear regression model trained on historical data. It is a simulation and NOT for financial advice."
        }

    except Exception as e:
        return {"error": f"An error occurred during ML-based price prediction for '{symbol}': {str(e)}"}