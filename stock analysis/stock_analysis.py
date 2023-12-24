import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as plt
import datetime

st.title("Stock Market Analysis")

logo={
    'AAPL':'img/apple.jpg',
    'MSFT':'img/microsoft.jpg',
    'SPY':'img/spy.webp',
    'WMT':'img/walmart.jpeg',
    'AMZN':'img/amazon.jpg',
    'GOOG':'img/google.webp',
    'FB':'img/facebook.png',
    'TSLA':'img/tesla.png',
    'NFLX':'img/netflix.jpg',
    'V':'img/visa.jpg',
    'KO':'img/Coca-Cola.png',
    'JPM':'img/jpmorgan.png',
    'INTC':'img/intel.png',
    'DIS':'img/disney.png',
    'SPOT':'img/spotify.png',
    'GS':'img/goldman.png',
    'NKE':'img/nike.jpg'
}
option = st.sidebar.selectbox('Select one symbol', ( 'AAPL', 'MSFT','SPY','WMT','AMZN','GOOG','FB','TSLA','NFLX',' V','KO','JPM','INTC','DIS','SPOT','GS','NKE'))
today = datetime.date.today()
before = today - datetime.timedelta(days=1000)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    stock_data = yf.download(option, start=start_date, end=end_date)

    st.subheader(f'Stock Data for {option}')

    if option in logo:
        logo_path = logo[option]
        st.image(logo_path, width=300) 
    else:
        st.write(f"No logo available for {option}")
    st.write(stock_data.head())

    fig = plt.line(stock_data, x=stock_data.index, y='Close', title=f'Stock Closing Prices for {option}')
    st.plotly_chart(fig)
else:
    st.sidebar.error('Error: End date must be after start date.')











