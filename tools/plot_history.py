import yfinance as yf
import matplotlib.pyplot as plt
import os

def plot_stock_history(symbol: str):
    """
    Generates and saves a 30-day historical price trend graph for a given stock symbol.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "GOOGL").

    Returns:
        dict: A dictionary containing the symbol, a success message, and the plot file path,
              or an error message if plotting fails.
    """
    try:
        stock = yf.Ticker(symbol)
        # Fetch 1 month (approx. 30 days) of history
        hist = stock.history(period="1mo")

        if hist.empty:
            return {"error": f"No historical data found for '{symbol}'. Please check the symbol."}

        plt.figure(figsize=(12, 6)) # Slightly larger figure for better readability
        plt.plot(hist.index, hist["Close"], label="Close Price", color="blue", linewidth=1.5)
        plt.title(f"{symbol.upper()} - 1 Month Price History", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Price", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        plt.xticks(rotation=45, ha='right') # Rotate dates for better readability
        plt.tight_layout() # Adjust layout to prevent labels from overlapping

        # Ensure the 'plots' directory exists
        os.makedirs("plots", exist_ok=True)
        filepath = f"plots/{symbol.upper()}_history.png"
        plt.savefig(filepath, dpi=300) # Save with higher resolution
        plt.close() # Close the plot to free up memory

        return {
            "symbol": symbol.upper(),
            "message": "Plot generated successfully",
            "plot_path": filepath
        }
    except Exception as e:
        return {"error": f"Failed to generate plot for '{symbol}': {str(e)}"}