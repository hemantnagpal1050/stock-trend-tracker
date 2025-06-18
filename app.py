import streamlit as st
from pytrends.request import TrendReq
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time

# Streamlit page config
st.set_page_config(page_title="Stock Trend Tracker", layout="wide")
st.title("📈 Stock Trends & Price Tracker")

# Define stock names and their Google Trends keywords + Yahoo Finance tickers
stock_keywords = {
    "RVNL": "RVNL share price",
    "IRFC": "IRFC stock",
    "Zomato": "Zomato stock",
    "Tata Motors": "Tata Motors share",
    "Adani Power": "Adani Power share"
}
tickers = {
    "RVNL": "RVNL.NS",
    "IRFC": "IRFC.NS",
    "Zomato": "ZOMATO.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Adani Power": "ADANIPOWER.NS"
}

# Let user select one stock
stock = st.selectbox("Select a stock to analyze:", options=list(stock_keywords.keys()))
keyword = stock_keywords[stock]
ticker = tickers[stock]

# Initialize pytrends
pytrends = TrendReq(hl='en-IN', tz=330)

# --- Google Trends ---
st.subheader(f"📊 Google Trends: {keyword}")
try:
    pytrends.build_payload([keyword], timeframe='today 1-m', geo='IN')
    time.sleep(1.5)  # Wait to prevent 429 errors
    trend_data = pytrends.interest_over_time()

    if 'isPartial' in trend_data.columns:
        trend_data = trend_data.drop(columns=['isPartial'])

    if not trend_data.empty:
        st.line_chart(trend_data[keyword])
    else:
        st.warning("No Google Trends data available.")
except Exception as e:
    st.warning(f"⚠️ Google Trends request failed: {e}")

# --- Stock Data ---
st.subheader(f"💹 Stock Price & Volume: {stock}")
try:
    stock_data = yf.download(ticker, period="1mo", interval="1d")

    if (
        not stock_data.empty and
        all(col in stock_data.columns for col in ['Close', 'Volume'])
    ):
        stock_data = stock_data.dropna(subset=['Close', 'Volume'])

        fig, ax1 = plt.subplots()
        ax1.plot(stock_data.index, stock_data['Close'], color='blue')
        ax1.set_ylabel('Price (₹)', color='blue')

        ax2 = ax1.twinx()
        ax2.bar(stock_data.index, stock_data['Volume'], color='gray', alpha=0.3)
        ax2.set_ylabel('Volume', color='gray')

        st.pyplot(fig)
    else:
        st.warning("Stock data is incomplete or unavailable.")
except Exception as e:
    st.warning(f"⚠️ Failed to fetch stock data: {e}")
