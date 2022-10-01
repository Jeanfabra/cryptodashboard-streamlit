import streamlit as st

def pageI():
    st.image('https://4.bp.blogspot.com/-1hBZaDQV6lY/XD930XvmeRI/AAAAAAAAAuM/Mb0nonSZOFkk0umjU7mXMdMhroDjvTq0ACKgBGAs/w5120-h1440-c/bitcoin-cryptocurrency-cube-abstract-4-4k.jpg')
    st.title('Welcome!!')
    st.markdown('''
    ## Crypto Dashboard - FTX API 💥
    ### [GitHub Link](https://github.com/Jeanfabra/cryptodashboard-streamlit)
    ### Feel free to use this tool for your cryptocurrency analysis! You can get real-time information about prices, price history, and cryptocurrency transaction volume. This is possible thanks to [FTX API](https://docs.ftx.com/#overview).
    ### For now, you can choose from the following cryptocurrencies:
    ### 🪙 Bitcoin: BTC &emsp; &emsp;  &emsp; &emsp;  &nbsp; &nbsp; 🪙 Ethereum: ETH  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 🪙 Solana: SOL 
    ### 🪙 Cardano: ADA &emsp; &emsp;   &emsp; &emsp; 🪙 Polkadot: DOT  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; 🪙 Matic: MATIC
    ### 🪙 ElRond: EGLD &emsp; &emsp;   &emsp; &emsp; 🪙 Doge: DOGE  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; &nbsp; &nbsp; &nbsp; 🪙 Ripple: XRP
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

    ## Navigation
    ### 🧷 1. Candlestick and volume chart: It has historical data of cryptocurrencies. High, Low, Close prices and volume can be viewed from a range of dates. The user can at will set this range as well as a resolution.
    ### 🧷 2. Cryptocurrency converter calculator: Here the user can choose if he wants to know the price in dollars of a chosen amount of cryptocurrencies, also the cryptocurrencies equivalent to an amount of dollars entered and also make an exchange between cryptocurrencies. Prices are updated in real time.
    # ''')
    st.info(
        "INFO: This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/Jeanfabra/cryptodashboard-streamlit/issues) or "
        "[pull requests](https://github.com/Jeanfabra/cryptodashboard-streamlit/pulls) "
        "to the [source code](https://github.com/Jeanfabra/cryptodashboard-streamlit)."
    )
