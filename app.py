import streamlit as st
import requests
import os
import base64

# ========== CONFIG ==========
FASTAPI_BASE_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Stock Dashboard", layout="centered")

# ========== THEME STATE ==========
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

dark_mode = st.toggle("🌙", value=st.session_state.theme == "Dark", label_visibility="collapsed")
st.session_state.theme = "Dark" if dark_mode else "Light"

# ========== THEME COLORS ==========
if st.session_state.theme == "Dark":
    text_color = "#FFFFFF"
    subtext_color = "#0D0404"
    card_bg = "#1A1A1A"
    accent = "#FFD700"
    gradient_start = "#FFD700"
    gradient_end = "#FF8C00"
else:
    text_color = "#1A1A1A"
    subtext_color = "#444444"
    card_bg = "#FFFFFF"
    accent = "#2196F3"
    gradient_start = "#2196F3"
    gradient_end = "#64B5F6"

# ========== BASE64 BACKGROUND ==========
def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

bg_image = get_base64_image("assets/dashboard_banner.png")

# ========== CUSTOM CSS ==========
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    html, body, [class*="st-"] {{
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {gradient_start}, {gradient_end});
        color: black !important;
        border: none;
        border-radius: 10px;
        padding: 0.65em 1.2em;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }}
    .stButton>button:hover {{
        filter: brightness(110%);
        transform: translateY(-2px);
    }}
    .main-header {{
        text-align: center;
        font-size: 2.4em;
        font-weight: bold;
        margin-bottom: 0.1em;
        color: {accent};
        text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
    }}
    .sub-caption {{
        text-align: center;
        font-size: 1.1em;
        color: {subtext_color};
        opacity: 0.85;
        margin-bottom: 1.5em;
    }}
    /* Input box font color override */
        input[type="text"] {{
        color: #111111 !important;  /* Almost black */
        background-color: #FFFFFF !important;  /* Light background for contrast */
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 0.5em;
}}

    </style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("<div class='main-header'>📊 Stock Market Analysis Using MCP</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-caption'>Powered by FastAPI + Streamlit</div>", unsafe_allow_html=True)

# ========== INPUT ==========
symbol = st.text_input("Enter Stock Symbol", value="").upper()

# ========== HELPER ==========
@st.cache_data(ttl=60)
def call_fastapi_tool(endpoint: str, symbol: str):
    try:
        res = requests.post(f"{FASTAPI_BASE_URL}/tools/{endpoint}", json={"symbol": symbol})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ========== TABS ==========
tabs = st.tabs(["📈 Live Data", "📊 History & Logging", "📤 Reports"])

# --- Tab 1: Live Data ---
with tabs[0]:
    st.subheader("Live Stock Data")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get Current Price"):
            result = call_fastapi_tool("get_current_price", symbol)
            if result and "price" in result:
                st.metric(label=f"{result['symbol']} Price", value=f"${result['price']:.2f}")
            elif result and "error" in result:
                st.error(result['error'])

    with col2:
        if st.button("Predict Price (ML)"):
            result = call_fastapi_tool("predict_price", symbol)
            if result and "predicted_price" in result:
                delta = result['predicted_price'] - result['current_price']
                st.metric(
                    label="Predicted Price",
                    value=f"${result['predicted_price']:.2f}",
                    delta=f"{delta:+.2f}"
                )
            elif result and "error" in result:
                st.error(result['error'])

# --- Tab 2: History & Logging ---
with tabs[1]:
    st.subheader("History & Logs")
    col3, col4 = st.columns(2)

    with col3:
        if st.button("Plot 1 Month History"):
            result = call_fastapi_tool("plot_history", symbol)
            if result and "plot_path" in result and os.path.exists(result['plot_path']):
                st.image(result['plot_path'], use_column_width=True)
            elif result and "error" in result:
                st.error(result['error'])

    with col4:
        if st.button("Log Current Price"):
            result = call_fastapi_tool("log_price", symbol)
            if result and "log_path" in result:
                st.success(result['message'])
                st.write(f"📁 Saved to: `{result['log_path']}`")
            elif result and "error" in result:
                st.error(result['error'])

# --- Tab 3: Reports ---
with tabs[2]:
    st.subheader("Reports")
    if st.button("Export Full Report"):
        result = call_fastapi_tool("export_report", symbol)
        if result and "report_path" in result:
            st.success(result['message'])
            st.write(f"📁 Saved to: `{result['report_path']}`")
        elif result and "error" in result:
            st.error(result['error'])

# ========== FOOTER ==========
st.markdown("---")
st.caption("📡 Ensure FastAPI is running at `http://127.0.0.1:8000`")
