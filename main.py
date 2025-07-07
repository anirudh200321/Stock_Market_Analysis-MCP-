from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import logging

# Import your tool functions
from tools.fetch_price import get_current_price
from tools.predict_price import predict_price
from tools.plot_history import plot_stock_history
from tools.log_price import log_current_price
from tools.export_report import export_stock_report # NEW IMPORT

# Initialize FastAPI app
app = FastAPI(
    title="MCP Stock Market Tool Server",
    description="A FastAPI server providing real-time stock market tools for MCP compatibility.",
    version="0.1.0"
)

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Pydantic Models for Request Bodies ---
class StockSymbol(BaseModel):
    """
    Pydantic model for validating stock symbol input.
    Ensures that the 'symbol' field is a string.
    """
    symbol: str

# --- API Endpoints ---

@app.post("/tools/get_current_price")
async def tool_get_current_price(stock_symbol: StockSymbol):
    """
    Fetches the current live price for a given stock symbol.

    Args:
        stock_symbol (StockSymbol): The request body containing the stock symbol (e.g., {"symbol": "AAPL"}).

    Returns:
        dict: A dictionary containing the stock symbol and its current price.
              Example: {"symbol": "AAPL", "price": 175.25}

    Raises:
        HTTPException: 404 Not Found if the symbol is invalid or data cannot be retrieved.
        HTTPException: 500 Internal Server Error for unexpected issues.
    """
    try:
        # Call the actual tool function
        price_data = get_current_price(stock_symbol.symbol)

        # Assuming get_current_price might return an error key if it fails internally
        if "error" in price_data:
            logger.error(f"Error fetching price for {stock_symbol.symbol}: {price_data['error']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=price_data["error"]
            )
        logger.info(f"Successfully fetched price for {stock_symbol.symbol}")
        return price_data
    except Exception as e:
        logger.exception(f"An unexpected error occurred in tool_get_current_price for {stock_symbol.symbol}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while fetching current price: {str(e)}"
        )

@app.post("/tools/predict_price")
async def tool_predict_price(stock_symbol: StockSymbol):
    """
    Predicts the next-day stock price for a given stock symbol.
    (Currently uses a dummy +2% prediction).

    Args:
        stock_symbol (StockSymbol): The request body containing the stock symbol (e.g., {"symbol": "GOOGL"}).

    Returns:
        dict: A dictionary containing the stock symbol and its predicted price.
              Example: {"symbol": "GOOGL", "predicted_price": 152.00}

    Raises:
        HTTPException: 404 Not Found if the symbol is invalid or prediction fails.
        HTTPException: 500 Internal Server Error for unexpected issues.
    """
    try:
        # Call the actual tool function
        prediction_data = predict_price(stock_symbol.symbol)

        if "error" in prediction_data:
            logger.error(f"Error predicting price for {stock_symbol.symbol}: {prediction_data['error']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=prediction_data["error"]
            )
        logger.info(f"Successfully predicted price for {stock_symbol.symbol}")
        return prediction_data
    except Exception as e:
        logger.exception(f"An unexpected error occurred in tool_predict_price for {stock_symbol.symbol}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while predicting price: {str(e)}"
        )

@app.post("/tools/plot_history")
async def tool_plot_history(stock_symbol: StockSymbol):
    """
    Generates and saves a 30-day historical price trend graph for a given stock symbol.

    Args:
        stock_symbol (StockSymbol): The request body containing the stock symbol (e.g., {"symbol": "MSFT"}).

    Returns:
        dict: A dictionary confirming the plot generation and its file path.
              Example: {"symbol": "MSFT", "plot_path": "plots/MSFT_history.png"}

    Raises:
        HTTPException: 404 Not Found if the symbol is invalid or plotting fails.
        HTTPException: 500 Internal Server Error for unexpected issues.
    """
    try:
        # Call the actual tool function
        plot_result = plot_stock_history(stock_symbol.symbol)

        if "error" in plot_result:
            logger.error(f"Error plotting history for {stock_symbol.symbol}: {plot_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=plot_result["error"]
            )
        logger.info(f"Successfully plotted history for {stock_symbol.symbol}")
        return plot_result
    except Exception as e:
        logger.exception(f"An unexpected error occurred in tool_plot_history for {stock_symbol.symbol}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while plotting history: {str(e)}"
        )

@app.post("/tools/log_price")
async def tool_log_price(stock_symbol: StockSymbol):
    """
    Logs the current price of a stock to a CSV file.

    Args:
        stock_symbol (StockSymbol): The request body containing the stock symbol (e.g., {"symbol": "AAPL"}).

    Returns:
        dict: A dictionary indicating success with the log file path.
              Example: {"symbol": "AAPL", "message": "Price logged successfully to logs/stock_prices.csv", "log_path": "logs/stock_prices.csv"}

    Raises:
        HTTPException: 500 Internal Server Error for any issues during logging.
    """
    try:
        log_result = log_current_price(stock_symbol.symbol)
        if "error" in log_result:
            logger.error(f"Error logging price for {stock_symbol.symbol}: {log_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=log_result["error"]
            )
        logger.info(f"Successfully logged price for {stock_symbol.symbol}")
        return log_result
    except Exception as e:
        logger.exception(f"An unexpected error occurred in tool_log_price for {stock_symbol.symbol}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while logging price: {str(e)}"
        )

@app.post("/tools/export_report") # NEW ENDPOINT
async def tool_export_report(stock_symbol: StockSymbol):
    """
    Generates a stock report including current and predicted prices, and saves it to a CSV file.

    Args:
        stock_symbol (StockSymbol): The request body containing the stock symbol (e.g., {"symbol": "AAPL"}).

    Returns:
        dict: A dictionary indicating success with the report file path.
              Example: {"symbol": "AAPL", "message": "Report generated successfully to reports/AAPL_report.csv", "report_path": "reports/AAPL_report.csv"}

    Raises:
        HTTPException: 500 Internal Server Error for any issues during report generation.
    """
    try:
        report_result = export_stock_report(stock_symbol.symbol)
        if "error" in report_result:
            logger.error(f"Error exporting report for {stock_symbol.symbol}: {report_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=report_result["error"]
            )
        logger.info(f"Successfully exported report for {stock_symbol.symbol}")
        return report_result
    except Exception as e:
        logger.exception(f"An unexpected error occurred in tool_export_report for {stock_symbol.symbol}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while exporting report: {str(e)}"
        )

@app.get("/")
def root():
    """
    Root endpoint for health checking the server.

    Returns:
        dict: A simple message indicating the server is running.
    """
    logger.info("Root endpoint accessed - server is running.")
    return {"message": "MCP Stock Market Server is running"}