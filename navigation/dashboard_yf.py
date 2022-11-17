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
    start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2022-09-01'), key = 'dstart_date')
    end_date = st.sidebar.date_input('End Date', value = pd.to_datetime('now'), key = 'dend_date')

    # Page
    col1, col2 = st.columns([1, 5])
    coin_image = f'img/{coin.lower()}.png'
    col1.header(f'{coin}/USD')
    col2.image(coin_image, width = 60)

    coin_df = get_historical(coin, start_date, end_date)

    check = st.radio('Filter', ['1D', '7D', '1M', '3M', '1Y', 'All', 'None'], horizontal = True, index = 6)

    if check == '1D':
        resolution = st.select_slider('Resolution', options = ["1m","2m", "5m", "15m", "30m", "60m", "90m", "1d"], value = "30m", key = '1dresolution')
        coin_df = get_historical(coin, period = '1d', start_date = None, end_date = None, interval = resolution)

    if check == '7D':
        back_days = date.today() - timedelta(days = 7)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = 900)
        resolution = st.select_slider('Resolution', options = [300, 900, 3600, 14400, 86400, 86400*2, 86400*3], key = '7dresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1M':
        back_days = date.today() - timedelta(days = 30)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [900, 3600, 14400, 86400, 86400*2, 86400*3, 86400*4], key = '1mresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '3M':
        back_days = date.today() - timedelta(days = 90)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [3600, 14400, 86400, 86400*2, 86400*3, 86400*4, 86400*7], key = '3mresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1Y':
        back_days = date.today() - timedelta(days = 365)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == 'All':
        back_days = date.today() - timedelta(days = 1095) # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(coin, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == 'None':
        pass

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


