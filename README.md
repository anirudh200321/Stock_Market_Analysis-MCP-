
## 📁 Project Directory Structure

```
STOCK_MARKET_ANALYSIS/
├── __pycache__/                   # Python cache files (auto-generated)
├── assets/                        # Static assets
│   └── dashboard_banner.png       # UI banner image
├── logs/                          # Logged stock price data
│   └── stock_prices.csv
├── plots/                         # Saved historical plots
│   ├── AAPL_history.png
│   ├── JPM_history.png
│   └── MSFT_history.png
├── reports/                       # Exported reports
│   └── AAPL_report.csv
├── tools/                         # Backend tool implementations
│   ├── __pycache__/
│   ├── export_report.py
│   ├── fetch_price.py
│   ├── log_price.py
│   ├── plot_history.py
│   └── predict_price.py
├── venv/                          # Python virtual environment (local)
├── agent.json                     # MCP metadata file
├── app.py                         # Streamlit frontend UI
├── main.py                        # FastAPI backend entry point
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```
