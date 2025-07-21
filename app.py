# app.py
import streamlit as st
import requests
import os
import pandas as pd

FASTAPI_BASE_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Stock Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-header { font-size: 2.5em; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .stMetric { border: 1px solid #2d3748; border-radius: 10px; padding: 15px; text-align: center; }
    .summary-text { text-align: justify; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>📊 Stock Market Analysis using MCP</div>", unsafe_allow_html=True)

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL, MSFT)", "").upper()

def call_fastapi_tool(endpoint: str, symbol: str):
    if not symbol:
        st.warning("Please enter a stock symbol.")
        return None
    try:
        url = f"{FASTAPI_BASE_URL}/tools/{endpoint}"
        res = requests.post(url, json={"symbol": symbol}, timeout=300)
        if res.status_code == 200:
            return res.json()
        else:
            error_detail = res.json().get('detail', res.text)
            st.error(f"API Error (Code {res.status_code}): {error_detail}")
            return None
    except requests.exceptions.RequestException:
        st.error(f"Connection Error: Could not connect to the API server at {FASTAPI_BASE_URL}. Is it running?")
        return None

tab0, tab1, tab2, tab3 = st.tabs(["📄 Stock Profile", "📈 Prediction", "📊 History", "📋 Reports"])

with tab0:
    st.subheader(f"Profile & Behavior Gist for {symbol}")
    if st.button("Get Stock Profile"):
        with st.spinner(f"Fetching profile for {symbol}..."):
            result = call_fastapi_tool("get_stock_summary", symbol)
            if result and "company_name" in result:
                st.header(result['company_name'])
                st.caption(f"{result['sector']} | {result['industry']}")

                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Market Cap", result['market_cap'])
                m_col2.metric("P/E Ratio", result['pe_ratio'])
                m_col3.metric("Beta (Volatility)", result['beta'])
                m_col4.metric("Analyst Grade", result.get('latest_recommendation', {}).get('grade', 'N/A'))
                
                # Business summary is now always visible
                st.subheader("Business Summary")
                st.markdown(f"<div class='summary-text'>{result['business_summary']}</div>", unsafe_allow_html=True)


with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Current Market Price")
        if st.button("Get Current Price"):
            with st.spinner("Fetching price..."):
                result = call_fastapi_tool("get_current_price", symbol)
                if result and "price" in result:
                    st.metric(label=f"Current {result['symbol']} Price", value=f"${result['price']:.2f}")
    with col2:
        st.subheader("5-Day Price Forecast")
        if st.button("Generate 5-Day Forecast"):
            with st.spinner("Running LSTM model... This may take a moment."):
                result = call_fastapi_tool("predict_price", symbol)
                if result and "predictions" in result:
                    st.metric(label="Current Price (for context)", value=f"${result.get('current_price', 0):.2f}")
                    pred_cols = st.columns(len(result["predictions"]))
                    sorted_preds = sorted(result["predictions"].items())
                    for i, (day, price) in enumerate(sorted_preds):
                        with pred_cols[i]:
                            st.metric(label=day, value=f"${price:.2f}")

with tab2:
    st.subheader("Historical Price Chart")
    if st.button("Plot 30-Day History"):
        with st.spinner("Generating plot..."):
            result = call_fastapi_tool("plot_history", symbol)
            if result and "plot_path" in result and os.path.exists(result['plot_path']):
                st.image(result['plot_path'], caption=f"30-Day Price History for {symbol}", use_column_width=True)

with tab3:
    st.subheader("Data Export")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Log Current Price to CSV"):
            with st.spinner("Logging price..."):
                result = call_fastapi_tool("log_price", symbol)
                if result and "log_path" in result:
                    st.success(result['message'])
    with col4:
        if st.button("Export Full Report to CSV"):
            with st.spinner("Generating report..."):
                result = call_fastapi_tool("export_report", symbol)
                if result and "report_path" in result:
                    st.success(result['message'])
                    with open(result['report_path'], "rb") as file:
                        st.download_button("Download Report", file, os.path.basename(result['report_path']), "text/csv")

st.markdown("---")
st.caption("Ensure the FastAPI backend is running. The LSTM model is for educational purposes and is not financial advice.")