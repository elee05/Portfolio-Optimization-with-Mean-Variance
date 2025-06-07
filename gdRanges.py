import numpy as np
import pandas as pd


df = pd.read_csv("Data\Weekly22-25 - Sheet1.csv", header = 0)

df=df.iloc[lambda x: x.index % 4 == 0]
df = df.iloc[1:].reset_index(drop=True)

def getMatrices(df):

    def get_var_name(var):
        for name, obj in globals().items():
            if obj is var:
                return name
        return None

    # Skip the first row which contains repeated headers
    
    df_cleaned=df
    
    
    dfs = []
    i = 0
    for c in df_cleaned:
        if c[0:5] != "Unnam":
            dfs.append([str(c[0:5]),df_cleaned.iloc[:, [i, i+1]].rename(columns={df.columns[i]: 'Date', df.columns[i+1]: 'Close'})])
        i += 1
    

    for pair in dfs:
        pair[1] = pair[1][pair[1]['Date'] != 'Date']
        pair[1]['Date'] = pd.to_datetime(pair[1]['Date'], errors='coerce')
        # pair[1]['Date'] = pd.to_datetime(pair[1]['Date'])
        pair[1]['Close'] = pd.to_numeric(pair[1]['Close'])
        pair[1]['Returns'] = pair[1]['Close'].pct_change()
        # print(pair[1])
    # print(dfs)

    n = len(dfs[1][1])

    ranges = []
    for i in range(n//2):
        timerange = []
        for pair in dfs:
            df = pair[1]
            if len(df) >= i + 11:
                timerange.append([pair[0],df.iloc[i:i+11]])
        ranges.append([i,timerange])

    # ranges is a of length based on num time periods,[timeperiod][tp number/list][if list --> stock][stock name/dataframe]

    def matrix(dfs):
        #stock covariance 
        #initialize matrix
        num = len(dfs)
        sigma = np.zeros((num,num),dtype=float)
        j = 0
        for pair in dfs:
            ar = np.average(pair[1]['Returns'].dropna())
            # print(pair[0])
            v = np.zeros((num),dtype=float)
            i = 0
            for cross in dfs:
                avgReturn_other = np.average(cross[1]['Returns'].dropna())
                otherDiffs = [x-avgReturn_other for x in cross[1]['Returns'].dropna()]
                mainDiffs = [x-ar for x in pair[1]['Returns'].dropna()]
                cov = sum([a*b for a,b in zip(otherDiffs,mainDiffs)])/len(pair[1])
                v[i] = cov
                if i < len(v)-1:
                    i+=1
            # print(v)
            sigma[j] = v
            if j < len(sigma)-1:
                j+=1
        # print(sigma)

        #holding avg returns
        m = np.zeros(num)
        for i in range(len(dfs)):
            average_return = np.average(dfs[i][1]["Returns"].dropna())
            # print(dfs[i][0], average_return)
            m[i] = average_return
        # print(m)
        return [m,sigma]
    ans = []
    for i in range(len(ranges)):
        ans.append(matrix(ranges[i][1]))
    #each element is a list for a time period, holding a mu and sigma [timeperiod][mu/sigma]
    return ans




