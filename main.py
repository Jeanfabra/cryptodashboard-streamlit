from datetime import datetime, date, timedelta
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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
    change24h = float(result['change24h'])
    return priceHigh24h, priceLow24h, volumeUsd24h, change24h

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
st.sidebar.image(
"https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
width=50)
# Main Page
def main_page():
    st.image('https://4.bp.blogspot.com/-1hBZaDQV6lY/XD930XvmeRI/AAAAAAAAAuM/Mb0nonSZOFkk0umjU7mXMdMhroDjvTq0ACKgBGAs/w5120-h1440-c/bitcoin-cryptocurrency-cube-abstract-4-4k.jpg')
    st.title('Welcome!!')
    st.markdown('''
    ## Crypto Dashboard - FTX API 💥
    ### Feel free to use this tool for your cryptocurrency analysis! You can get real-time information about prices, price history, and cryptocurrency transaction volume. This is possible thanks to [FTX API](https://docs.ftx.com/#overview).
    ### For now, you can choose from the following cryptocurrencies:
    ### 🪙 Bitcoin: BTC &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; &nbsp; 🪙 Ethereum: ETH  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 🪙 Solana: SOL 
    ### 🪙 Cardano: ADA &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 🪙 Polkadot: DOT  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; 🪙 Matic: MATIC
    ### 🪙 ElRond: EGLD &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 🪙 Doge: DOGE  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; &nbsp; &nbsp; &nbsp; 🪙 Ripple: XRP
    ### 🪙 Uniswap: UNI

    ### To get started go to navigation in the sidebar. Then, select the desire crypto in the dropdown. By default, the start date is set for 2022/07/01 you can change this value at your own discretion. Note that the oldest information offered by the API is for mid-2019.
    ----
    ## Data quality and detail report
    ### For this report, the questions established by [IBM](https://www.ibm.com/docs/es/spss-modeler/saas?topic=quality-writing-data-report) were used.
    ### 📌 1. Have you identified missing attributes and empty fields? If so, do the missing values ​​have meaning?
    ### Historical data is not observed for older coins such as BTC, ETH and XRP. As mentioned above, the FTX API provides information since September 2019. This is not a problem since the price did not vary much before 2019 and the rest of the chosen cryptocurrencies have later creation times.

    ### 📌 2. Have you detected deviations to determine if they are "noise" or phenomena that deserve an in-depth analysis?
    ### No noise has been detected in the data. In general, the FTX API presents a good performance.

    ### 📌 3. Have you performed a correct check of the values?
    ### The correct evaluation was made from the currency calculator. The results were compared with existing online calculators. This provides us with information on both the correct price of the cryptocurrency and the execution of the calculator.

    ### 📌 4. Have you considered excluding data that has no bearing on your hypotheses?
    ### [FTX API](https://docs.ftx.com/#overview) has a lot of information. From all this flow of data, only those of interest were extracted, such as the historical prices of the market and the individual prices of cryptocurrencies.

    ### 📌 5. Is the data stored in flat files? If so, do the delimiters maintain consistency between the files? Does each record contain the same number of fields?
    ### The data is obtained from the direct connection with the FTX API. This allows us to have a real-time data flow with the minimum resolution provided by the API (15 seconds).

    ----

    ## Dashboard data
    ### 🧷 1. Candlestick and volume chart: It has historical data of cryptocurrencies. High, Low, Close prices and volume can be viewed from a range of dates. The user can at will set this range as well as a resolution.
    ### 🧷 2. Cryptocurrency converter calculator: Here the user can choose if he wants to know the price in dollars of a chosen amount of cryptocurrencies, also the cryptocurrencies equivalent to an amount of dollars entered and also make an exchange between cryptocurrencies. Prices are updated in real time.



    ### For more information: https://github.com/Jeanfabra/cryptodashboard-streamlit ''')
    st.info(
        "INFO: This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/Jeanfabra/cryptodashboard-streamlit/issues) of or "
        "[pull requests](https://github.com/Jeanfabra/cryptodashboard-streamlit/pulls) "
        "to the [source code](https://github.com/Jeanfabra/cryptodashboard-streamlit)."
    )

# Dashboard
def pageII():
    st.title('🪙 Crypto Dashboard', anchor = "title")

    # Sidebar

    tickers = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'UNI')
    dropdown = st.sidebar.selectbox('Pick a coin from the list', tickers)
    start_date = st.sidebar.date_input('Start Date', value = pd.to_datetime('2022-07-01'), key = 'dstart_date')
    end_date = st.sidebar.date_input('End Date', value = pd.to_datetime('now'), key = 'dend_date')
    dresolution = st.sidebar.slider('Resolution', min_value = 86400, max_value = 86400*30, step = 86400, key = 'dresolution')
    

    # Page
    st.subheader(f'{dropdown}/USD', anchor = 'coin')
    coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = dresolution)

    check = st.radio('Filter', ['1D', '7D', '1M', '3M', '1Y', 'All', 'None'], horizontal = True, index = 6)

    if check == '1D':
        back_days = date.today() - timedelta(days = 1)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [15, 60, 300, 900, 3600, 14400, 86400], key = '1dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '7D':
        back_days = date.today() - timedelta(days = 7)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = 900)
        resolution = st.select_slider('Resolution', options = [300, 900, 3600, 14400, 86400, 86400*2, 86400*3], key = '7dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1M':
        back_days = date.today() - timedelta(days = 30)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [900, 3600, 14400, 86400, 86400*2, 86400*3, 86400*4], key = '1mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '3M':
        back_days = date.today() - timedelta(days = 90)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [3600, 14400, 86400, 86400*2, 86400*3, 86400*4, 86400*7], key = '3mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1Y':
        back_days = date.today() - timedelta(days = 365)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == 'All':
        back_days = date.today() - timedelta(days = 1095) # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)
    
    if check == 'None':
        pass

    # Moving average - 30weeks
    coin_df['30wma'] = coin_df['close'].rolling(30).mean()

    variance = round(np.var(coin_df['close']),3)
    priceHigh24h, priceLow24h, volumeUsd24h, change24h = get_market(dropdown)
    price = get_market_price(dropdown)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col4: st.metric('Variance', variance)
    with col2: st.metric('24h High', priceHigh24h)
    with col3: st.metric('24h Low', priceLow24h)
    with col5: st.metric('24h Volume', volumeUsd24h)
    with col1: st.metric('Price', price, round(change24h,5))


    # Candle and volume chart
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing = 0.1, row_heights = [100,30])
    fig.add_trace(
        go.Candlestick(x = coin_df['date'],
                       open = coin_df['open'], high = coin_df['high'],
                       low = coin_df['low'], close = coin_df['close'],
                       name = 'Candlestick Chart',
                       ), row = 1, col = 1
    )

    fig.update_layout(xaxis_rangeslider_visible = False)

    fig.add_trace(
        go.Scatter(
            x = coin_df['date'],
            y = coin_df['30wma'],
            line = dict(color = '#e0e0e0', width = 2, dash = 'dot'),
            name = "30-week MA"
        ), row = 1, col = 1
    )

    # Bar chart https://plotly.com/python-api-reference/generated/plotly.graph_objects.bar.html#plotly.graph_objects.bar.Marker
    fig.add_trace(
        go.Bar(
            x = coin_df['date'],
            y = coin_df['volume'],
            marker = dict(color = coin_df['volume'], colorscale = 'aggrnyl_r')
        ), row = 2, col = 1
    )
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    st.plotly_chart(fig, use_container_width = True)

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

