# tools/export_report.py
import pandas as pd
import os
from datetime import datetime

# Import the functions we need from other tools
from .fetch_price import get_current_price
from .predict_price import predict_stock_price

REPORTS_DIR = "reports"
REPORT_FILE = os.path.join(REPORTS_DIR, "full_stock_reports.csv")

def export_stock_report(symbol: str):
    """
    Generates a comprehensive report with current price and 5-day forecast,
    and appends it to a CSV file.
    """
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)

        # --- Fetch all necessary data first ---
        current_price_data = get_current_price(symbol)
        if "error" in current_price_data:
            return current_price_data  # Pass the error up

        prediction_data = predict_stock_price(symbol)
        if "error" in prediction_data:
            return prediction_data  # Pass the error up

        # --- Prepare a dictionary with all data for the report ---
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol.upper(),
            "current_price": current_price_data.get("price")
        }

        # --- Flatten the nested prediction dictionary into the main report data ---
        # This handles the new 5-day forecast structure
        predictions = prediction_data.get("predictions", {})
        for day, price in predictions.items():
            # Create a clean header key, e.g., 'Day +1' becomes 'prediction_day_1'
            header_key = f"prediction_{day.replace(' ', '').replace('+', '')}"
            report_data[header_key] = price

        # --- Use pandas to write to CSV ---
        # This easily handles dynamic columns and appends new rows
        df = pd.DataFrame([report_data])

        # Check if the file exists to decide whether to write headers
        file_exists = os.path.isfile(REPORT_FILE)

        # Append to the CSV file
        df.to_csv(REPORT_FILE, mode='a', header=not file_exists, index=False)

        return {
            "symbol": symbol.upper(),
            "message": f"Report for {symbol.upper()} saved successfully.",
            "report_path": REPORT_FILE
        }

    except Exception as e:
        return {"error": f"Failed to generate report for '{symbol}': {str(e)}"}