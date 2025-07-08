
# 📈 Stock Market Analysis Tool

This project features a **real-time, MCP-compatible stock market analysis tool** with a **FastAPI** backend and a **Streamlit** frontend. It allows users to fetch live stock prices, get simple ML-based predictions, view historical plots, log price data, and export reports.

## ✨ Overview

The application is structured into a FastAPI backend that exposes various stock analysis tools as API endpoints, and a Streamlit frontend that provides an interactive dashboard to consume these tools. It is designed with Multi-Agent Communication Protocol (MCP) compatibility in mind, using an `agent.json` file to describe its capabilities.
![Uploading image.png…]()


## 📁 Project Directory Structure

```

STOCK\_MARKET\_ANALYSIS/
├── **pycache**/             \# Python cache files (auto-generated)
├── assets/                  \# Static assets (e.g., dashboard\_banner.png)
├── logs/                    \# Logged stock price data (e.g., stock\_prices.csv)
├── plots/                   \# Saved historical plots (e.g., AAPL\_history.png)
├── reports/                 \# Exported reports (e.g., AAPL\_report.csv)
├── tools/                   \# Backend tool implementations
│   ├── **pycache**/
│   ├── export\_report.py
│   ├── fetch\_price.py
│   ├── log\_price.py
│   ├── plot\_history.py
│   └── predict\_price.py
├── venv/                    \# Python virtual environment (local)
├── agent.json               \# MCP metadata file
├── app.py                   \# Streamlit frontend UI
├── main.py                  \# FastAPI backend entry point
├── requirements.txt         \# Python dependencies
└── README.md                \# Project documentation

````

## 🚀 Setup and Running Locally

This project runs entirely on your local machine and is **not deployed**.

### 1. Prerequisites

Ensure you have Python 3.8+ installed.

### 2. Clone the Repository

```bash
git clone <repository_url_here>
cd STOCK_MARKET_ANALYSIS
````

### 3\. Set Up Virtual Environment

```bash
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

### 4\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5\. Run the Backend (FastAPI)

Open your first terminal, activate the virtual environment, and run:

```bash
uvicorn main:app --reload
```

The FastAPI server will run on `http://127.0.0.1:8000`.

### 6\. Run the Frontend (Streamlit)

Open a **second terminal**, activate the virtual environment, and run:

```bash
streamlit run app.py
```

The Streamlit UI will open in your browser (usually `http://localhost:8501`).

## ⏭️ Future Enhancements

  * Integration with other MCP agents.
  * Implementation of more advanced ML models for prediction.
  * Real-time data streaming capabilities.
  * User authentication and database integration.
  * Interactive plotting with libraries like Plotly.
  * Deployment to cloud platforms.

<!-- end list -->

```
```
