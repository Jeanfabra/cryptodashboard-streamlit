import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_historical(coin: str, start_date, end_date, period = None, interval = '1d'):

    ''' This function extracts data from yfinance API and returns a dataframe
      with information about historical prices according to the chosen crypto'''

    coin = coin + "-USD"
    stock = yf.Ticker(coin)
    historical = stock.history(period = period, start = start_date, end = end_date, interval = interval).reset_index()
    if "Datetime" in historical.columns:
        historical.rename({"Datetime": "Date"}, axis = 1, inplace = True)

    return historical

def pageII():
    
    st.title('Crypto Dashboard', anchor = "title")

    # Sidebar
    tickers = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'BNB')
    coin = st.sidebar.selectbox('Pick a coin from the list', tickers)

    # Page
    col1, col2 = st.columns([1, 5])
    coin_image = f'img/{coin.lower()}.png'
    col1.header(f'{coin}/USD')
    col2.image(coin_image, width = 60)

    check = st.radio('Filter', ['1D', '5D', '1M', '3M', '6M', '1Y', '2Y', 'All', 'None'], horizontal = True, index = 8)

    if check == 'None':
        start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2022-01-01'), key = 'dstart_date')
        end_date = st.sidebar.date_input('End Date', value = pd.to_datetime('now'), key = 'dend_date')
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1mo"], value = "1d", key = 'Nresolution')
        coin_df = get_historical(coin, start_date, end_date, interval = resolution)

    if check == '1D':
        resolution = st.select_slider('Resolution', options = ["1m","2m", "5m", "15m", "30m", "60m", "90m", "1d"], value = "30m", key = '1dresolution')
        coin_df = get_historical(coin, period = '1d', start_date = None, end_date = None, interval = resolution)

    if check == '5D':
        resolution = st.select_slider('Resolution', options = ["30m", "60m", "90m", "1d"], value = "30m", key = '5dresolution')
        coin_df = get_historical(coin, period = '5d', start_date = None, end_date = None, interval = resolution)

    if check == '1M':
        resolution = st.select_slider('Resolution', options = ["90m", "1d", "5d", "1wk", "1mo"], value = "1d", key = '1mresolution')
        coin_df = get_historical(coin, period = '1mo', start_date = None, end_date = None, interval = resolution)

    if check == '3M':
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1wk", "1mo"], value = "1d", key = '3mresolution')
        coin_df = get_historical(coin, period = '3mo', start_date = None, end_date = None, interval = resolution)

    if check == '6M':
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1wk", "1mo", "3mo"], value = "1d", key = '6mresolution')
        coin_df = get_historical(coin, period = '6mo', start_date = None, end_date = None, interval = resolution)

    if check == '1Y':
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1wk", "1mo", "3mo"], value = "1d", key = '1yrresolution')
        coin_df = get_historical(coin, period = '1y', start_date = None, end_date = None, interval = resolution)

    if check == '2Y':
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1wk", "1mo", "3mo"], value = "1d", key = '2yrresolution')
        coin_df = get_historical(coin, period = '2y', start_date = None, end_date = None, interval = resolution)

    if check == 'All':
        back_days = date.today() - timedelta(days = 1095) # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = ["1d", "5d", "1wk", "1mo", "3mo"], value = "1d", key = 'allrresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, interval = resolution)


    # Moving average - 30weeks
    coin_df['30wma'] = coin_df['Close'].rolling(30).mean()
    variance = round(np.var(coin_df['Close']),3)
    
    # Candle and volume chart
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing = 0.1, row_heights = [100,30])
    fig.add_trace(
        go.Candlestick(x = coin_df['Date'],
                        open = coin_df['Open'], high = coin_df['High'],
                        low = coin_df['Low'], close = coin_df['Close'],
                        name = 'Candlestick',
                        ), row = 1, col = 1
    )

    fig.update_layout(xaxis_rangeslider_visible = False)

    fig.add_trace(
        go.Scatter(
            x = coin_df['Date'],
            y = coin_df['30wma'],
            line = dict(color = '#e0e0e0', width = 2, dash = 'dot'),
            name = "30-week MA"
        ), row = 1, col = 1
    )

    # Bar chart https://plotly.com/python-api-reference/generated/plotly.graph_objects.bar.html#plotly.graph_objects.bar.Marker
    fig.add_trace(
        go.Bar(
            x = coin_df['Date'],
            y = coin_df['Volume'],
            marker = dict(color = coin_df['Volume'], colorscale = 'aggrnyl_r'),
            name = 'Volume'
        ), row = 2, col = 1
    )
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    st.plotly_chart(fig, use_container_width = True)


