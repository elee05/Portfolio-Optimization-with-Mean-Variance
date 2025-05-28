

import numpy as np
import pandas as pd


# df = pd.read_csv("Data\Weekly24-25.csv")
# df=df.iloc[lambda x: x.index % 4 == 0]

def getMatrix(df):

    def get_var_name(var):
        for name, obj in globals().items():
            if obj is var:
                return name
        return None

    # Skip the first row which contains repeated headers
    df_cleaned = df
    # Extract each pair of Date and Close as its own table
    AAPL = df_cleaned.iloc[:, [0, 1]].rename(columns={df.columns[0]: 'Date', df.columns[1]: 'Close'})
    MSFT = df_cleaned.iloc[:, [3, 4]].rename(columns={df.columns[3]: 'Date', df.columns[4]: 'Close'})
    NVDA = df_cleaned.iloc[:, [6, 7]].rename(columns={df.columns[6]: 'Date', df.columns[7]: 'Close'})
    HD   = df_cleaned.iloc[:, [9, 10]].rename(columns={df.columns[9]: 'Date', df.columns[10]: 'Close'})
    COST = df_cleaned.iloc[:, [12, 13]].rename(columns={df.columns[12]: 'Date', df.columns[13]: 'Close'})

    # Optionally convert Close to numeric and Date to datetime
    for stock in [AAPL, MSFT, NVDA, HD, COST]:
        stock['Date'] = pd.to_datetime(stock['Date'])
        stock['Close'] = pd.to_numeric(stock['Close'])

    # Example: display AAPL data
    AAPL['returns'] = AAPL['Close'].pct_change()
    MSFT['returns'] = MSFT['Close'].pct_change()
    NVDA['returns'] = NVDA['Close'].pct_change()
    HD['returns'] = HD['Close'].pct_change()
    COST['returns'] = COST['Close'].pct_change()
    # print(MSFT)


    #stock covariance 
    #initialize matrix
    sigma = np.zeros((5,5),dtype=float)
    stocks = [AAPL,MSFT, NVDA, HD, COST]
    for j in range(len(stocks)):
        ar = np.average(stocks[j]['returns'].dropna())
        # print(get_var_name(stocks[j]))
        v = np.zeros((5),dtype=float)
        for i in range(len(stocks)):
            avgReturn_other = np.average(stocks[i]['returns'].dropna())
            otherDiffs = [x-avgReturn_other for x in stocks[i]['returns'].dropna()]
            mainDiffs = [x-ar for x in stocks[j]['returns'].dropna()]
            cov = sum([a*b for a,b in zip(otherDiffs,mainDiffs)])/len(AAPL)
            # print(cov)
            v[i] = cov
            
        # print(v)
        sigma[j] = v
    # print(sigma)



    #holding avg returns
    m = np.zeros(5)
    for i in range(len(stocks)):
        average_return = np.average(stocks[i]['returns'].dropna())
        name = get_var_name(stocks[i])
        # print(name,f"{average_return:.4f}")
        m[i] = average_return
    # print(f'returns vector: {m}')
    return [m,sigma]


