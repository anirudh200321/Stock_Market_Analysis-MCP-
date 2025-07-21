# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import logging

# Import your tool functions
from tools.fetch_price import get_current_price
from tools.predict_price import predict_stock_price
from tools.plot_history import plot_stock_history
from tools.log_price import log_current_price
from tools.export_report import export_stock_report
from tools.get_stock_summary import get_stock_summary

app = FastAPI(
    title="MCP Stock Market Tool Server",
    description="A FastAPI server providing stock tools, including a 5-day price forecast and profile summary.",
    version="1.1.0"
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StockSymbol(BaseModel):
    symbol: str

@app.post("/tools/get_current_price")
async def tool_get_current_price(stock_symbol: StockSymbol):
    try:
        price_data = get_current_price(stock_symbol.symbol)
        if "error" in price_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=price_data["error"])
        return price_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/tools/predict_price")
async def tool_predict_price(stock_symbol: StockSymbol):
    try:
        prediction_data = predict_stock_price(stock_symbol.symbol)
        if "error" in prediction_data:
            status_code = status.HTTP_400_BAD_REQUEST if "data" in prediction_data["error"] else status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code=status_code, detail=prediction_data["error"])
        return prediction_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error predicting price: {str(e)}")

@app.post("/tools/plot_history")
async def tool_plot_history(stock_symbol: StockSymbol):
    try:
        plot_result = plot_stock_history(stock_symbol.symbol)
        if "error" in plot_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=plot_result["error"])
        return plot_result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/tools/log_price")
async def tool_log_price(stock_symbol: StockSymbol):
    try:
        log_result = log_current_price(stock_symbol.symbol)
        if "error" in log_result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=log_result["error"])
        return log_result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/tools/export_report")
async def tool_export_report(stock_symbol: StockSymbol):
    try:
        report_result = export_stock_report(stock_symbol.symbol)
        if "error" in report_result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=report_result["error"])
        return report_result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/tools/get_stock_summary")
async def tool_get_stock_summary(stock_symbol: StockSymbol):
    try:
        summary_data = get_stock_summary(stock_symbol.symbol)
        if "error" in summary_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=summary_data["error"])
        return summary_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error fetching summary: {str(e)}")

@app.get("/")
def root():
    return {"message": "MCP Stock Market Server is running"}