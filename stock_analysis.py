import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression


st.title("Stock Market Analysis")

option = st.sidebar.selectbox(
    'Select one symbol',
    ('AAPL', 'MSFT', 'SPY', 'WMT', 'AMZN', 'GOOG', 'FB', 'TSLA', 'NFLX', 'V', 'KO', 'JPM', 'INTC', 'DIS', 'SPOT', 'GS', 'NKE')
)

today = datetime.date.today()
before = today - datetime.timedelta(days=1000)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date >= end_date:
    st.sidebar.error('Error: End date must be after start date.')
else:
    stock_data = yf.download(option, start=start_date, end=end_date)

    st.subheader(f'Stock Data for {option}')

    if stock_data.empty:
        st.error("No stock data available. Please adjust the symbol or date range.")
    elif 'Close' not in stock_data.columns:
        st.error(f"'Close' column missing for {option}. Unable to plot data.")
    else:
        st.write(stock_data.head())

        close_data = stock_data['Close'].values.flatten()

        fig = px.line(
            x=stock_data.index, 
            y=close_data,         
            title=f'Stock Closing Prices for {option}'
        )
        st.plotly_chart(fig)

        # Calculate moving averages
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

        # Create Buy/Sell signals
        stock_data['Signal'] = 'Hold'
        stock_data.loc[stock_data['MA50'] > stock_data['MA200'], 'Signal'] = 'Buy'
        stock_data.loc[stock_data['MA50'] < stock_data['MA200'], 'Signal'] = 'Sell'

        # Add moving averages to the plot
        fig.add_scatter(x=stock_data.index, y=stock_data['MA50'], mode='lines', name='MA50')
        fig.add_scatter(x=stock_data.index, y=stock_data['MA200'], mode='lines', name='MA200')

        # Show updated plot with MAs
        st.plotly_chart(fig)

        # Display Buy/Sell signals as a table (drop rows with NaN moving averages)
        signals = stock_data[['Close', 'MA50', 'MA200', 'Signal']].dropna()
        st.subheader("Buy/Sell Signals based on MA50 and MA200 Crossover")
        st.dataframe(signals)

        # Filter only buy signals
        buy_signals = signals[signals['Signal'] == 'Buy']

        # Filter only sell signals
        sell_signals = signals[signals['Signal'] == 'Sell']

        st.subheader("Buy Signal Dates")
        st.dataframe(buy_signals[['Close', 'MA50', 'MA200', 'Signal']])

        st.subheader("Sell Signal Dates")
        st.dataframe(sell_signals[['Close', 'MA50', 'MA200', 'Signal']])

        st.sidebar.subheader("Investment Tracker")

        entry_price = st.sidebar.number_input("Entry Price", min_value=0.0, value=100.0)
        quantity = st.sidebar.number_input("Quantity Bought", min_value=1, value=10)

        if 'Close' in stock_data.columns:
            current_price = float(stock_data['Close'].iloc[-1].item())
            unrealized_pnl = (current_price - entry_price) * quantity
            roi = (unrealized_pnl / (entry_price * quantity)) * 100

            st.subheader("Investment Performance")
            st.write(f"**Entry Price:** ₹{entry_price}")
            st.write(f"**Current Price:** ₹{current_price:.2f}")
            st.write(f"**Quantity:** {quantity}")

            # Color the P&L value based on profit or loss
            if unrealized_pnl > 0:
                pnl_str = f"<span style='color: green;'>₹{unrealized_pnl:.2f} (Profit)</span>"
            elif unrealized_pnl < 0:
                pnl_str = f"<span style='color: red;'>₹{unrealized_pnl:.2f} (Loss)</span>"
            else:
                pnl_str = f"<span>₹{unrealized_pnl:.2f} (Break-even)</span>"

            st.markdown(f"**Unrealized P&L:** {pnl_str}", unsafe_allow_html=True)

            # Color ROI similarly
            if roi > 0:
                roi_str = f"<span style='color: green;'>{roi:.2f}%</span>"
            elif roi < 0:
                roi_str = f"<span style='color: red;'>{roi:.2f}%</span>"
            else:
                roi_str = f"<span>{roi:.2f}%</span>"

            st.markdown(f"**Return on Interest:** {roi_str}", unsafe_allow_html=True)
            st.write(f"**Break-even Price:** ₹{entry_price}")
