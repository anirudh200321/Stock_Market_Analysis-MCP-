Stock Market Analysis using MCP
A comprehensive stock analysis tool that provides real-time data, a 5-day price forecast using a custom-trained LSTM model, and qualitative stock profile summaries. The project is built with a decoupled architecture, using FastAPI for the backend API and Streamlit for the interactive web dashboard.

🌟 Features
This dashboard provides a multi-faceted view of any given stock ticker:

📄 Stock Profile: Get a qualitative "gist" of a stock, including company business summary, key metrics like Market Cap and P/E Ratio, and the latest analyst recommendation.

📈 5-Day Price Forecast: Utilizes a custom-trained LSTM (Long Short-Term Memory) neural network to predict the closing price for the next five trading days.

📊 Historical Charting: Instantly generate and view a 30-day historical price chart to analyze recent trends.

📋 Data Export: Log the current price to a persistent CSV file or generate a full report with the 5-day forecast.

🤖 MCP Implementation: Fully compatible with the Model-Context-Protocol. The system exposes its tools via a discoverable agents.json manifest and a FastAPI backend, allowing other AI models to use its capabilities.

🏗️ Architecture
The project uses a modern, decoupled architecture to separate concerns:

FastAPI Backend (main.py):

A high-performance backend server that exposes all functionality through a REST API.

It handles the core logic, including fetching data from Yahoo Finance, running the ML model for predictions, and generating plots/reports.

All functionalities are organized into modular "tools" within the tools/ directory.

Streamlit Frontend (app.py):

A user-friendly and interactive web dashboard.

It acts as a client that communicates with the FastAPI backend to fetch and display data.

This separation allows the backend logic to be independent of the user interface.

🤖 MCP Implementation
This project is designed to be fully compatible with the Model-Context-Protocol (MCP), allowing its tools to be programmatically discovered and used by other AI models or automated systems. Here’s how the implementation works:

The Manifest (agents.json): This file serves as the public "menu" of the agent's capabilities. It follows the OpenAPI 3.0 specification to define:

What tools are available: Each function (like get_current_price, predict_price, etc.) is listed as an API path.

What each tool does: A human-readable summary explains the purpose of each tool.

How to use each tool: It specifies the HTTP method (POST), the required input (requestBody), and the expected output (responses).

The Engine (FastAPI Backend): The FastAPI server acts as the live execution engine. It listens for incoming API requests that match the paths defined in agents.json. When a request is received (e.g., a POST request to /tools/predict_price with a stock symbol), the server:

Validates the incoming data.

Calls the corresponding Python function from the tools/ directory.

Executes the function's logic (e.g., runs the ML model).

Returns the result as a standard JSON response.

By separating the definition of the tools (agents.json) from their execution (FastAPI), any MCP-aware system can intelligently interact with this stock analysis agent without needing to know its internal code.

🚀 Setup and Installation
Follow these steps to get the project running on your local machine.

Prerequisites
Python 3.10 or higher.

pip and venv for package management.

Step 1: Set Up the Project
First, ensure all the project files are in a single directory.

Step 2: Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

# Navigate to your project directory

cd path/to/stock_market_analysis

# Create a virtual environment

python -m venv venv

# Activate the virtual environment

# On Windows:

.\venv\Scripts\Activate

# On macOS/Linux:

source venv/bin/activate

Step 3: Install Dependencies
Install all the required packages using the requirements.txt file.

pip install -r requirements.txt

Step 4: Train the LSTM Model
Before you can get predictions, you must train the machine learning model. This script fetches the last 10 years of data for a stock (AAPL by default) and trains the LSTM model, saving the artifacts in the models/ directory.

python train_model.py

Note: To train the model for a different stock (e.g., MSFT), simply edit the last line of train_model.py to train_and_save_model(symbol="MSFT").

Step 5: Run the Application
The application requires two separate terminals to run the backend and frontend simultaneously.

Terminal 1: Start the FastAPI Backend

uvicorn main:app --reload

You should see a confirmation that the Uvicorn server is running on http://127.0.0.1:8000.

Terminal 2: Start the Streamlit Frontend

streamlit run app.py

This will automatically open a new tab in your browser pointing to the dashboard.

💻 How to Use
Enter a Stock Symbol: Use the text input at the top of the dashboard to enter a ticker symbol (e.g., GOOGL, MSFT, TSLA).

Navigate Tabs:

📄 Stock Profile: Click "Get Stock Profile" to see a summary of the company.

📈 Prediction: Get the latest price or generate a new 5-day forecast.

📊 History: Generate the 30-day price chart.

📋 Reports: Log the current price or export a full report to a CSV file.

📁 Project Structure
stock_market_analysis/
│
├── models/ # Stores the trained ML model and scaler
│ ├── lstm_stock_predictor.keras
│ ├── model_metadata.json
│ └── scaler.pkl
│
├── plots/ # Saved historical price charts
│ └── AAPL_history.png
│
├── reports/ # Saved CSV reports
│ └── full_stock_reports.csv
│
├── tools/ # Modular functions (tools) for the API
│ ├── **init**.py
│ ├── export_report.py
│ ├── fetch_price.py
│ ├── get_stock_summary.py
│ ├── log_price.py
│ ├── plot_history.py
│ └── predict_price.py
│
├── venv/ # Virtual environment directory
│
├── agents.json # MCP agent definition file
├── app.py # The Streamlit frontend application
├── main.py # The FastAPI backend server
├── README.md # This file
├── requirements.txt # Project dependencies
└── train_model.py # Script to train the LSTM model

📜 Disclaimer
This project is for educational purposes only and should not be considered financial advice. Stock market predictions are inherently uncertain, and the forecasts generated by the LSTM model are not guaranteed to be accurate. Always conduct your own research before making any investment decisions.
