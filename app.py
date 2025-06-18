import streamlit as st
from pytrends.request import TrendReq
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="Stock Interest Tracker", layout="wide")
st.title("📈 Stock Trends & Price Tracker (Google Trends + Market Data)")

# Define stock keywords (Google search terms) and tickers
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

# Stock selector
selected_stocks = st.multiselect("Select stocks to analyze:", options=list(stock_keywords.keys()), default=["RVNL", "IRFC"])

# Initialize pytrends connection
pytrends = TrendReq(hl='en-IN', tz=330)

# Layout
col1, col2 = st.columns(2)

# Loop through selected stocks
for stock in selected_stocks:
    keyword = stock_keywords[stock]
    ticker = tickers[stock]

    # --- Google Trends Data ---
    pytrends.build_payload([keyword], timeframe='today 1-m', geo='IN')
    trend_data = pytrends.interest_over_time()
    if 'isPartial' in trend_data.columns:
        trend_data.drop(columns=['isPartial'], inplace=True)

    with col1:
        st.subheader(f"📊 Google Trends: {keyword}")
        if not trend_data.empty:
            st.line_chart(trend_data[keyword])
        else:
            st.warning(f"No Google Trends data found for {keyword}")

    # --- Stock Data from Yahoo Finance ---
    stock_data = yf.download(ticker, period="1mo", interval="1d")

    with col2:
        st.subheader(f"💹 Price & Volume: {stock}")

        # Ensure stock data exists and required columns are present
        if (
            not stock_data.empty and
            all(col in stock_data.columns for col in ['Close', 'Volume'])
        ):
            stock_data = stock_data.dropna(subset=['Close', 'Volume'])

            fig, ax1 = plt.subplots()
            ax1.plot(stock_data.index, stock_data['Close'], color='blue', label='Close Price')
            ax1.set_ylabel('Price (₹)', color='blue')

            ax2 = ax1.twinx()
            ax2.bar(stock_data.index, stock_data['Volume'], color='gray', alpha=0.3)
            ax2.set_ylabel('Volume', color='gray')

            st.pyplot(fig)
        else:
            st.warning(f"📉 Insufficient stock data available for {stock} ({ticker})")
