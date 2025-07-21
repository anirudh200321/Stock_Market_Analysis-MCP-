# tools/get_stock_summary.py
import yfinance as yf
import pandas as pd

def get_stock_summary(symbol: str):
    """
    Fetches a summary of a stock's profile, including business summary,
    key metrics, and analyst ratings.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # A simple check for valid data
        if not info or info.get('trailingPegRatio') is None:
            return {"error": f"Could not retrieve valid summary data for '{symbol}'. It may be an invalid ticker."}

        # --- Key Metrics ---
        market_cap = info.get('marketCap', 'N/A')
        if isinstance(market_cap, (int, float)):
            market_cap = f"${market_cap/1e9:.2f}B"

        summary_data = {
            "symbol": info.get('symbol'),
            "company_name": info.get('shortName'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "market_cap": market_cap,
            "pe_ratio": f"{info.get('trailingPE', 0):.2f}",
            "beta": f"{info.get('beta', 0):.2f}", # Beta measures volatility
            "52_week_high": f"${info.get('fiftyTwoWeekHigh', 0):.2f}",
            "52_week_low": f"${info.get('fiftyTwoWeekLow', 0):.2f}",
            "business_summary": info.get('longBusinessSummary', 'No summary available.')
        }

        # --- Analyst Recommendation ---
        try:
            recs = ticker.recommendations
            if recs is not None and not recs.empty:
                latest_rec = recs.iloc[-1]
                summary_data['latest_recommendation'] = {
                    "firm": latest_rec.get('Firm'),
                    "grade": latest_rec.get('To Grade'),
                    "date": latest_rec.name.strftime('%Y-%m-%d')
                }
            else:
                summary_data['latest_recommendation'] = {"grade": "N/A"}
        except Exception:
            summary_data['latest_recommendation'] = {"grade": "N/A"}

        return summary_data

    except Exception as e:
        return {"error": f"An unexpected error occurred while fetching summary for '{symbol}': {str(e)}"}