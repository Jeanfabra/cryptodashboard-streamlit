from datetime import datetime, date, timedelta
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Defining our 10 crypto variables
BTC = "BTC/USD"
ETH = "ETH/USD"
SOL = "SOL/USD"
ADA = "ADA-PERP"
DOT = "DOT/USD"
MATIC = "MATIC/USD"
EGLD = "EGLD-PERP"
DOGE = "DOGE/USD"
XRP = "XRP/USD"
UNI = "UNI/USD"

URL_BASE = "https://ftx.com/api"

def get_historical(coin, start_date, end_date, resolution = 86400):

    ''' This function extracts data from FTX API and returns a dataframe
      with information about historical prices according to the chosen crypto'''

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    start_time = pd.to_datetime(start_date.strftime("%Y-%m-%d")).timestamp()
    end_time = pd.to_datetime(end_date.strftime("%Y-%m-%d")).timestamp()

    url =  f'{URL_BASE}/markets/{coin}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'])
    
    result['date'] = pd.to_datetime(result['time']/1000, unit = 's', origin = 'unix')
    result.drop(['startTime', 'time'], axis = 1, inplace = True)
    return result

def get_market(coin: str):

    '''This function extracts data from FTX API and returns a dataframe
    with insights according to the chosen crypto'''

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    url =  f'{URL_BASE}/markets/{coin}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'], index = [0])
    priceHigh24h = float(result['priceHigh24h'])
    priceLow24h = float(result['priceLow24h'])
    volumeUsd24h = float(result['volumeUsd24h'])
    return priceHigh24h, priceLow24h, volumeUsd24h

def get_market_price(coin: str):

    '''This function extracts data from FTX API and returns a dataframe
    with insights according to the chosen crypto'''

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    url =  f'{URL_BASE}/markets/{coin}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'], index = [0])
    price = result['price']
    return price

# Streamlit pages
st.set_page_config(layout = 'wide')
# Main Page
def main_page():
    st.title('Crypto Dashboard - FTX API')
    st.subheader('DTS03-PI03: github/Jeanfabra')

# Dashboard
def pageII():
    st.title('🪙 Crypto Dashboard', anchor = "title")

    # Sidebar
    tickers = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'UNI')
    dropdown = st.sidebar.selectbox('Pick a coin from the list', tickers)
    start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2022-07-01'), key = 'dstart_date')
    end_date = st.sidebar.date_input('End Date', value = pd.to_datetime('today'), key = 'dend_date')
    dresolution = st.sidebar.slider('Resolution', min_value = 86400, max_value = 86400*30, step = 86400, key = 'dresolution')

    # Page
    st.subheader(f'{dropdown}/USD', anchor = 'coin')
    coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = dresolution)

    # 
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1: check_1d = st.checkbox('1D')
    with col2: check_7d = st.checkbox('7D')
    with col3: check_1m = st.checkbox('1M')
    with col4: check_3m = st.checkbox('3M')
    with col5: check_1y = st.checkbox('1Y')
    with col6: check_all = st.checkbox('All')

    if check_1d:
        back_days = date.today() - timedelta(days = 1)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        resolution = st.select_slider('Resolution', options = [15, 60, 300, 900, 3600, 14400, 86400], key = '1dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check_7d:
        back_days = date.today() - timedelta(days = 7)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = 900)
        resolution = st.select_slider('Resolution', options = [300, 900, 3600, 14400, 86400, 86400*2, 86400*3], key = '7dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check_1m:
        back_days = date.today() - timedelta(days = 30)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        resolution = st.select_slider('Resolution', options = [900, 3600, 14400, 86400, 86400*2, 86400*3, 86400*4], key = '1mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check_3m:
        back_days = date.today() - timedelta(days = 90)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        resolution = st.select_slider('Resolution', options = [3600, 14400, 86400, 86400*2, 86400*3, 86400*4, 86400*7], key = '3mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check_1y:
        back_days = date.today() - timedelta(days = 365)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check_all:
        back_days = date.today() - timedelta(days = 1095) # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('today')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)
        

    # Moving average - 30weeks
    coin_df['30wma'] = coin_df['close'].rolling(30).mean()

    variance = round(np.var(coin_df['close']),3)
    priceHigh24h, priceLow24h, volumeUsd24h = get_market(dropdown)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.text(f'Variance: {variance}')
    with col2: st.text(f'24h High: {priceHigh24h}')
    with col3: st.text(f'24h Low: {priceLow24h}')
    with col4: st.text(f'24h Volume: {volumeUsd24h}')

    # Candle chart
    fig = go.Figure(data = [go.Candlestick(x = coin_df['date'],
                            open = coin_df['open'], high = coin_df['high'],
                            low = coin_df['low'], close = coin_df['close']
                            )])

    fig.update_layout(title = 'Candle chart', yaxis_title = f'{dropdown}  Price (USD)')
    fig.add_trace(
        go.Scatter(
            x = coin_df['date'],
            y = coin_df['30wma'],
            line = dict(color = '#e0e0e0', width = 2, dash = 'dot'),
            name = "30-week MA"
        )
    )
    st.plotly_chart(fig, use_container_width = True)

    # Bar chart
    barchart = px.bar(
        title = 'Volume Chart',
        data_frame = coin_df,
        x = 'date',
        y = 'volume',
        color = 'volume',
        color_continuous_scale = px.colors.sequential.Aggrnyl_r,
    )
    st.plotly_chart(barchart, use_container_width = True)

    # Show data
    if st.checkbox('Show data'):
        st.dataframe(coin_df)

    # Crypto/USD Calculator
    st.header('🪙 Cryptocurrency converter calculator')
    #st.subheader('Please select two currencies from the following boxes')
    col1, col2 = st.columns(2)

    tickers2 = ('USD', 'BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'UNI')
    with col1: box01 = st.selectbox('Currency to convert',tickers2, key = 'coin1')
    with col2: box02 = st.selectbox('Currency of interest', tickers2, key = 'coin2')
    
    columns = st.columns((2, 1, 2))
    quantity = columns[1].number_input('Quantity')


    if box01 != 'USD' and box02 != 'USD':
        price1 = get_market_price(box01)
        price2 = get_market_price(box02)
        convert = float(quantity*price1/price2)
    elif box01 == 'USD' and box02 != 'USD':
        price2 = get_market_price(box02)
        convert = float(quantity/price2)
    elif box01 != 'USD' and box02 == 'USD':
        price1 = get_market_price(box01)
        convert = float(quantity*price1)
    else:
        convert = quantity

    columns = st.columns((2, 1, 2))
    #quantity = columns[1].text(f'{quantity} {box01} = {convert} {box02}')
    quantity = columns[1].metric('',convert)

pages = {
    'I. Main Page': main_page,
    'II. Crypto Dashboard': pageII
}

selected_page = st.sidebar.radio("Navigation", pages.keys())
pages[selected_page]()

