import numpy as np
import pandas as pd
import gdfull
import opTestFull 

df = pd.read_csv("Data\Weekly24-25.csv")
#convert to monthly
df=df.iloc[lambda x: x.index % 4 == 0]
df = df.iloc[1:].reset_index(drop=True)

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
stocks = ['AAPL','MSFT', 'NVDA','HD', 'COST']

#calculate change
changeMap = {}
for stock in stocks:
    changeMap[stock] = float(mapfuture[stock]) - float(mappos[stock])


#calculate position from import
vars=gdfull.getMatrix(dfHist)
move = opTestFull.getWeights(vars[0],vars[1])

opweights = move[0].round(4)
portfolio_size = 10000

#invest
weighted_port = opweights*portfolio_size
print(f"weighted port: {weighted_port}")

#convert percent investments to map for easier handling
wportMap = {}
for i in range(len(weighted_port)):
    wportMap[stocks[i]] = weighted_port[i]

#calculate return
ret = 0
for stock in stocks:
    print(f"{stock}: {float(wportMap[stock])/float(mappos[stock]) * float(changeMap[stock])}")
    ret += float(wportMap[stock])/float(mappos[stock]) * float(changeMap[stock])

print(f"prices on entry: {mappos}")
print(f"prices after one month{mapfuture}")   
print(f"map of price change{changeMap}") 
print(f"return in cash: {ret}")




