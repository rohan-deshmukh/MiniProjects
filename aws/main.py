from pandas_datareader import data as pdr
import pandas as pd

tickers = ['AAPL', 'MSFT', '^GSPC']

start_date = '2015-01-01'
end_date = '2016-12-31'

data = pd.DataFrame()
for i in range(len(tickers)):
    panel_data = pdr.DataReader(tickers[i], 'yahoo', start_date, end_date)
    panel_data['Ticker'] = tickers[i]
    data = data.append(panel_data)

df = pd.concat([pd.DataFrame([i], columns=['A']) for i in range(5)], ignore_index=True)
print(df)
