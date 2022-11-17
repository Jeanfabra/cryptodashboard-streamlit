import streamlit as st
from navigation.dashboard_yf import get_market, get_historical

# Crypto/USD Calculator
def calculator():
    # Crypto/USD Calculator
    st.title('🪙 Cryptocurrency converter calculator')
    col1, col2 = st.columns(2)

    tickers2 = ('USD', 'BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'BNB')
    with col1: box01 = st.selectbox('From',tickers2, key = 'coin1')
    with col2: box02 = st.selectbox('To', tickers2, key = 'coin2')
    
    columns = st.columns((2, 1, 2))
    quantity = columns[0].number_input('Quantity')

    if box01 != 'USD' and box02 != 'USD':
        price1 = get_historical(box01, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        price2 = get_historical(box02, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity*price1/price2)
    elif box01 == 'USD' and box02 != 'USD':
        price2 = get_historical(box02, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity/price2)
    elif box01 != 'USD' and box02 == 'USD':
        price1 = get_historical(box01, start_date= None, end_date = None, period = '1d')['Close'].iloc[-1]
        convert = float(quantity*price1)
    else:
        convert = quantity

    columns = st.columns((1, 1))
    quantity = columns[0].metric('',convert)