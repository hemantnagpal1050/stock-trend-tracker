import streamlit as st
from pytrends.request import TrendReq
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Interest Tracker", layout="wide")
st.title("📈 Stock Trends & Price Tracker (Google Trends + Market Data)")

# Define stock terms and tickers
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

selected_stocks = st.multiselect("Select stocks to analyze:", options=list(stock_keywords.keys()), default=["RVNL", "IRFC"])
pytrends = TrendReq(hl='en-IN', tz=330)

col1, col2 = st.columns(2)

for stock in selected_stocks:
    keyword = stock_keywords[stock]
    ticker = tickers[stock]

    # Google Trends
    pytrends.build_payload([keyword], timeframe='today 1-m', geo='IN')
    trend_data = pytrends.interest_over_time()
    if 'isPartial' in trend_data.columns:
        trend_data.drop(columns=['isPartial'], inplace=True)

    # Stock Data
    stock_data = yf.download(ticker, period="1mo", interval="1d")

    with col1:
        st.subheader(f"📊 Google Trends: {keyword}")
        st.line_chart(trend_data[keyword])
        
    with col2:
        st.subheader(f"💹 Price & Volume: {stock}")
        fig, ax1 = plt.subplots()
        ax1.plot(stock_data.index, stock_data['Close'], color='blue', label='Close Price')
        ax1.set_ylabel('Price (₹)', color='blue')
        ax2 = ax1.twinx()
        ax2.bar(stock_data.index, stock_data['Volume'], color='gray', alpha=0.3)
        ax2.set_ylabel('Volume', color='gray')
        st.pyplot(fig)
