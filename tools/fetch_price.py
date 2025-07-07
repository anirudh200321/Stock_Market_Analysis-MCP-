import yfinance as yf

def get_current_price(symbol: str):
    """
    Fetches the current stock price for a given symbol from Yahoo Finance.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "GOOGL").

    Returns:
        dict: A dictionary containing the symbol and its current price,
              or an error message if data cannot be retrieved.
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return {"error": f"No data found for '{symbol}'. Please check the symbol."}

        # Get the latest closing price
        current_price = data["Close"].iloc[-1]
        return {
            "symbol": symbol.upper(),
            "price": round(current_price, 2)
        }
    except Exception as e:
        # Catch any exceptions during data fetching (e.g., network issues, invalid symbol format)
        return {"error": f"Failed to fetch current price for '{symbol}': {str(e)}"}