import os
import csv
from datetime import datetime
from tools.fetch_price import get_current_price
from tools.predict_price import predict_price

def export_stock_report(symbol: str):
    """
    Generates a stock report including current and predicted prices, and saves it to a CSV file.

    The report file will be located in 'reports/{SYMBOL}_report.csv'.
    Each entry includes a timestamp, stock symbol, current price, and predicted price.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "GOOGL").

    Returns:
        dict: A dictionary indicating success with the report file path,
              or an error message if report generation fails.
    """
    reports_dir = "reports"
    report_filepath = os.path.join(reports_dir, f"{symbol.upper()}_report.csv")
    
    try:
        # Ensure the reports directory exists
        os.makedirs(reports_dir, exist_ok=True)

        # Fetch current price
        current_data = get_current_price(symbol)
        if "error" in current_data:
            return {"error": f"Could not generate report for '{symbol}': {current_data['error']}"}
        current_price = current_data["price"]

        # Fetch predicted price
        prediction_data = predict_price(symbol)
        if "error" in prediction_data:
            return {"error": f"Could not generate report for '{symbol}': {prediction_data['error']}"}
        predicted_price = prediction_data["predicted_price"]

        timestamp = datetime.now().isoformat()

        # Check if file exists to determine if header needs to be written
        file_exists = os.path.exists(report_filepath)

        with open(report_filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new or empty
            if not file_exists or os.stat(report_filepath).st_size == 0:
                writer.writerow(["Timestamp", "Symbol", "Current Price", "Predicted Price"])
            
            writer.writerow([timestamp, symbol.upper(), current_price, predicted_price])
        
        return {
            "symbol": symbol.upper(),
            "message": f"Report generated successfully to {report_filepath}",
            "report_path": report_filepath
        }

    except Exception as e:
        return {"error": f"An error occurred while generating report for '{symbol}': {str(e)}"}