

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Trading Dashboard", layout="wide")
st.title("📈 Trading Dashboard")

symbol = st.sidebar.text_input("Stock Symbol", "RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y"])

@st.cache_data(ttl=60)
def get_data(ticker, period):
    return yf.download(ticker, period=period, progress=False)

try:
    data = get_data(symbol, period)

    if data.empty:
        st.error("No stock data found. Check the symbol or internet connection.")
    else:
        close = data["Close"].squeeze().dropna()

        if close.empty:
            st.error("Closing price data is unavailable.")
        else:
            current = float(close.iloc[-1])
            previous = float(close.iloc[-2]) if len(close) > 1 else current

            col1, col2 = st.columns(2)
            col1.metric("Latest Price", f"{current:.2f}",
                        f"{current - previous:+.2f}")
            col2.metric("Highest Price", f"{float(close.max()):.2f}")

            st.subheader("Stock Price Chart")
            st.line_chart(close)

            st.subheader("Recent Data")
            st.dataframe(data.tail(10), use_container_width=True)

except Exception as e:
    st.error(f"Unable to load data: {e}")