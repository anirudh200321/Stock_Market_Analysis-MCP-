import os
import csv
from datetime import datetime
from tools.fetch_price import get_current_price

def log_current_price(symbol: str):
    """
    Fetches the current price of a stock and logs it to a CSV file.

    The log file will be located in 'logs/stock_prices.csv'.
    Each entry includes a timestamp, stock symbol, and its current price.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "GOOGL").

    Returns:
        dict: A dictionary indicating success with the log file path,
              or an error message if logging fails.
    """
    log_dir = "logs"
    log_filepath = os.path.join(log_dir, "stock_prices.csv")
    
    try:
        # Ensure the logs directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Fetch current price using the existing tool
        price_data = get_current_price(symbol)

        if "error" in price_data:
            return {"error": f"Could not log price for '{symbol}': {price_data['error']}"}

        current_price = price_data["price"]
        timestamp = datetime.now().isoformat() # ISO format for easy parsing

        # Check if file exists to determine if header needs to be written
        file_exists = os.path.exists(log_filepath)

        with open(log_filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new
            if not file_exists or os.stat(log_filepath).st_size == 0:
                writer.writerow(["Timestamp", "Symbol", "Price"])
            
            writer.writerow([timestamp, symbol.upper(), current_price])
        
        return {
            "symbol": symbol.upper(),
            "message": f"Price logged successfully to {log_filepath}",
            "log_path": log_filepath
        }

    except Exception as e:
        return {"error": f"An error occurred while logging price for '{symbol}': {str(e)}"}