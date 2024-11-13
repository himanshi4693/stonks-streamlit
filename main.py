import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from datetime import date

# Define sectors and representative stocks within each sector
sector_stocks = {
    "Technology": ["TCS.NS", "INFY.NS", "WIPRO.NS"],
    "Finance": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS"],
    "Pharmaceuticals": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "BPCL.NS"],
}

# Streamlit app title and description
st.title("Indian Stock Market Analysis")
st.write("Analyze Indian stocks and explore sector trends and opportunities with live Yahoo Finance data.")

# Sidebar - Date range selection
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Helper function to fetch stock data from Yahoo Finance
@st.cache
def fetch_stock_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# 1. Stock Price Analysis
st.header("1. Stock Price Analysis")
selected_stock = st.selectbox("Select a stock:", ["TCS.NS", "HDFCBANK.NS", "RELIANCE.NS", "INFY.NS", "WIPRO.NS"])

if selected_stock:
    data = fetch_stock_data(selected_stock)
    st.subheader(f"Stock Price for {selected_stock}")
    st.line_chart(data['Close'], width=0, height=250)
    st.write("Latest data from Yahoo Finance.")

# 2. Sector-Wise Performance
st.header("2. Sector-Wise Performance")
selected_sector = st.selectbox("Select a sector:", list(sector_stocks.keys()))

if selected_sector:
    st.write(f"Performance of {selected_sector} sector")
    sector_performance = []

    # Fetch stock data for each ticker in the selected sector
    for ticker in sector_stocks[selected_sector]:
        stock_data = fetch_stock_data(ticker)
        if not stock_data.empty:
            recent_price = stock_data['Close'].iloc[-1]
            initial_price = stock_data['Close'].iloc[0]
            change = ((recent_price - initial_price) / initial_price) * 100
            sector_performance.append({'Ticker': ticker, 'Performance (%)': change})

    if sector_performance:
        sector_df = pd.DataFrame(sector_performance)
        st.bar_chart(sector_df.set_index('Ticker')['Performance (%)'])
    else:
        st.write("No data available for the selected sector.")

# 3. Periodic Sector Performance Analysis
st.header("3. Sector Performance Analysis Over Different Periods")

# Dropdown for selecting performance period
performance_period = st.selectbox("Choose Performance Period:",
                                  ("Daily", "Weekly", "Monthly", "3-Month", "6-Month", "Yearly"))

# Define period in terms of trading days
period_map = {
    "Daily": 1,
    "Weekly": 5,       # ~5 trading days in a week
    "Monthly": 20,     # ~20 trading days in a month
    "3-Month": 60,     # ~60 trading days in 3 months
    "6-Month": 120,    # ~120 trading days in 6 months
    "Yearly": 252      # ~252 trading days in a year
}

period_days = period_map[performance_period]

# Calculate performance for each sector over the selected period
performance_data = []

for sector, tickers in sector_stocks.items():
    sector_returns = []
    for ticker in tickers:
        stock_data = fetch_stock_data(ticker)
        if len(stock_data) > period_days:
            period_data = stock_data[-period_days:]  # Get data for the specified period
            start_price = period_data['Close'].iloc[0]
            end_price = period_data['Close'].iloc[-1]
            period_change = ((end_price - start_price) / start_price) * 100
            sector_returns.append(period_change)
    if sector_returns:
        avg_sector_return = sum(sector_returns) / len(sector_returns)
        performance_data.append({'Sector': sector, f'{performance_period} Performance (%)': avg_sector_return})

# Display the "Hot" Sectors for the selected period
if performance_data:
    performance_df = pd.DataFrame(performance_data).sort_values(by=f'{performance_period} Performance (%)', ascending=False)
    st.write(f"Top Performing Sectors ({performance_period}):")
    st.table(performance_df)
else:
    st.write(f"No data available for {performance_period} sector performance.")

# Conclusion
st.write("""
### Insights
Based on the data, these are the top-performing sectors for the selected period
""")

