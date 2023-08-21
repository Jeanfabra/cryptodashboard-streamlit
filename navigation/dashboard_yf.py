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

    coin += "-USD"
    stock = yf.Ticker(coin)

    historical = stock.history(period = period, start = start_date, end = end_date, interval = interval).reset_index()
    if "Datetime" in historical.columns:
        historical.rename({"Datetime": "Date"}, axis=1, inplace=True)

    return historical

def get_market(coin: str):
    '''This function extracts data from yfinance and returns a dataframe
    with insights according to the chosen crypto'''

    coin += "-USD"
    stock = yf.Ticker(coin)

    # yfinance info: can't find 'regularMarketPrice' replaced by 'regularMarketDayLow'
    # https://github.com/ranaroussi/yfinance/issues/1519
    
    info = {
        "priceHigh24h": stock.info.get('dayHigh', None),
        "priceLow24h": stock.info.get('dayLow', None),
        "volumeUsd24h": stock.info.get('volume24Hr', None),
        "price": stock.info.get('regularMarketDayLow', None)
    }
    
    return info

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

    # Metrics
    col1, col2, col3 = st.columns([2, 2, 2])
    info = get_market(coin)
    price_difference_24h = (info['price'] - info['priceHigh24h'])/info['price'] * 100
    col1.metric('Price', f'{info["price"]:,}', f'{round(price_difference_24h,2)}%')
    col2.metric('24h High', f'{info["priceHigh24h"]:,}')
    col3.metric('24h Low', f'{info["priceLow24h"]:,}')

    st.metric('24h Volume', f'{info["volumeUsd24h"]:,}')

    # Check periods

    # The code has been simplified by using a dictionary to store the resolution options and default values 
    # for each filter option, instead of having multiple if conditionals for each option.

    check = st.radio('Filter', ['1D', '5D', '1M', '3M', '6M', '1Y', '2Y', 'All', 'None'], horizontal=True, index=8)

    resolution_options = {
        '1D': (["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d"], "30m"),
        '5D': (["30m", "60m", "90m", "1d"], "30m"),
        '1M': (["90m", "1d", "5d", "1wk", "1mo"], "1d"),
        '3M': (["1d", "5d", "1wk", "1mo"], "1d"),
        '6M': (["1d", "5d", "1wk", "1mo", "3mo"], "1d"),
        '1Y': (["1d", "5d", "1wk", "1mo", "3mo"], "1d"),
        '2Y': (["1d", "5d", "1wk", "1mo", "3mo"], "1d")
    }

    if check == 'None':
        start_date = st.sidebar.date_input('Start Date', value=pd.to_datetime('2022-01-01'), key='dstart_date')
        end_date = st.sidebar.date_input('End Date', value=pd.to_datetime('now'), key='dend_date')
        resolution = st.select_slider('Resolution', options=["1d", "5d", "1mo"], value="1d", key='Nresolution')
        coin_df = get_historical(coin, start_date, end_date, interval=resolution)
    elif check == 'All':
        back_days = date.today() - timedelta(days=1095)  # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options=["1d", "5d", "1wk", "1mo", "3mo"], value="1d",
                                    key='allrresolution')
        coin_df = get_historical(coin, start_date=start_date, end_date=end_date, interval=resolution)
    else:
        options, default_value = resolution_options[check]
        period = check.lower()
        resolution = st.select_slider('Resolution', options=options, value=default_value,
                                    key=f'{period}resolution')
        coin_df = get_historical(coin, period=period, start_date=None, end_date=None, interval=resolution)

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

    # Show data
    if st.checkbox('Show data'):
        st.dataframe(coin_df)