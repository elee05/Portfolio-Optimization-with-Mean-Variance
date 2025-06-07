import numpy as np
import pandas as pd
import gdfull
import opTestFull 
import gdRanges
from matplotlib import pyplot as plt

df = pd.read_csv("Data\Weekly22-25 - Sheet1.csv")
#convert to monthly
df=df.iloc[lambda x: x.index % 4 == 0]
df = df.iloc[1:].reset_index(drop=True)



def Results(df):
    #separate forecasting data and testing data
    dfHist = df.drop(index=len(df)-1)
    posData = df.iloc[len(df)-2]
    testData = df.iloc[len(df)-1]

    def InstanceToMap(data):
        map = {}
        indexVals = data.index
        for i in range(0,len(data),3):
            map[indexVals[i]] = data[i+1]
        return map

    #variables for use
    mapfuture = InstanceToMap(testData)
    mappos = InstanceToMap(posData)

    stocks = []
    for c in df:
        if c[0:5] != "Unnam":
                    stocks.append(str(c[0:5]))

    #calculate change
    changeMap = {}
    for stock in stocks:
        changeMap[stock] = float(mapfuture[stock]) - float(mappos[stock])

    # # #calculate position from import
    vars=gdfull.getMatrix(dfHist)
    move = opTestFull.getWeights(vars[0],vars[1])

    opweights = move[0].round(4)
    portfolio_size = 10000

    # # #invest
    weighted_port = opweights*portfolio_size
    print(f"weighted portolio: {weighted_port}")

    # #convert percent investments to map for easier handling
    wportMap = {}
    for i in range(len(weighted_port)):
        wportMap[stocks[i]] = weighted_port[i]

    #calculate return
    ret = 0
    for stock in stocks:
        print(f"{stock} return: {float(wportMap[stock])/float(mappos[stock]) * float(changeMap[stock])}")
        ret += float(wportMap[stock])/float(mappos[stock]) * float(changeMap[stock])

    print(f"prices on entry: {mappos}")
    print(f"prices after one month{mapfuture}")   
    print(f"map of price change{changeMap}") 
    print(f"return in cash: {ret}")

def periodResults(df):
    #separate forecasting data and testing data
    dfHist = df.drop(index=len(df)-1)
    posData = df.iloc[len(df)-2]
    testData = df.iloc[len(df)-1]

    periods = gdRanges.getMatrices(dfHist)
    print(periods[0])
    mov = []
    for i in range(len(periods)):
        PI = periods[i]
        op = opTestFull.getWeights(PI[0],PI[1])
        mov.append(op[0])

    stocks = []
    for c in df:
        if c[0:5] != "Unnam":
                    stocks.append(str(c[0:5]))

    portMat = np.array(mov)

    plt.figure(1)
    for i in range(len(portMat.transpose())):
        plt.plot(portMat.transpose()[i], label = stocks[i])
    plt.title("Optimal Portfolio Weights over Time")
    plt.legend()
    plt.show()

def retResults(df):
    dfs = []
    i = 0
    for c in df:
        if c[0:5] != "Unnam":
            dfs.append([str(c[0:5]),df.iloc[:, [i, i+1]].rename(columns={df.columns[i]: 'Date', df.columns[i+1]: 'Close'})])
        i += 1
    

    for pair in dfs:
        pair[1] = pair[1][pair[1]['Date'] != 'Date']
        pair[1]['Date'] = pd.to_datetime(pair[1]['Date'], errors='coerce')
        # pair[1]['Date'] = pd.to_datetime(pair[1]['Date'])
        pair[1]['Close'] = pd.to_numeric(pair[1]['Close'])
        pair[1]['Returns'] = pair[1]['Close'].pct_change()
    retlog = []
    for pair in dfs:
        stockRets = []
        for r in pair[1]['Returns']:
            stockRets.append(r)
        retlog.append([pair[0],stockRets])

    plt.figure(2)  
    for log in retlog:
        plt.plot(log[1], label = log[0] )

    plt.title('Stock Returns')
    plt.xlabel('Time(Months)')
    plt.ylabel('Percent Returns')
    plt.legend()
    plt.show()
    print("hi")

periodResults(df)
retResults(df)



     





