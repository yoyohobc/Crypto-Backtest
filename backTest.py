import csv
from datetime import datetime as dt
#特定時間突破區間追價策略
#幣種＆初始金額
crypto = 'ETH'
usd = 725
csvname = crypto+"_1m"
with open(csvname+".csv", newline='',encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    datas = list(rows)
dateList = [str(dt.fromtimestamp(int(p[0])/1000)) for p in datas]
price = [float(p[4]) for p in datas]
print("start...")
def checkTime(index):
    return dateList[index][11:16] in ['08:00','22:00']

def calculator(index,initPrice,initMs):
    if(initPrice == 0 or initMs == 0):
        return 0
    if (int(datas[index][0]) - initMs) <= 3600000:
        percentGap = (price[index] - initPrice)/initPrice
        if percentGap >= 0.011:
            return 1
        elif percentGap <= -0.011:
            return 2
        else:
            return 0
def buySignal(index,initPrice,initMs):
    return calculator(index,initPrice,initMs) == 1

def sellSignal(index,initPrice,initMs):
    return calculator(index,initPrice,initMs) == 2

def buyOutSignal(index,Max):
    percentGap = (price[index] - Max)/Max
    return percentGap <= -0.004
def sellOutSignal(index,Min):
    percentGap = (price[index] - Min)/Min
    return percentGap >= 0.004     

def getIn(index,isBuy):
    global buy,sell,inPrice,Min,Max
    buy,sell,inPrice,Min,Max = isBuy,not isBuy,price[index],0 if isBuy else price[index],price[index] if isBuy else 0
    action = 'buy' if isBuy else 'sell'
    global benefit
    benefit.append([action,price[i],usd,"0%",dateList[i]])

def initial():
    global buy,sell,inPrice,initMs,initPrice,Min,Max
    buy,sell,inPrice,initMs,initPrice,Min,Max = False,False,0,0,0,0,0

def getOut(index,inPrice,isSell):
    action = 'sellOut' if isSell else 'buyOut'
    percent = ((price[index]/inPrice) - 1)
    percent = percent*-1 if isSell else percent
    global usd
    usd += percent*usd
    percentage = str(percent*100) + "%"
    global benefit
    benefit.append([action,price[index],usd,percentage,dateList[index]])
    initial()

buy = False
sell = False
inPrice = 0
benefit = [['Action','Price','USD','Percent','Time']]
initMs = 0
initPrice = 0
Min = 0
Max = 0
length = len(price)
#1767790
for i in range(length):
    if buy:
        if(price[i]>Max):
            Max = price[i]
        if buyOutSignal(i,Max):
            getOut(i,inPrice,False)
    elif sell:
        if(price[i]<Min):
            Min = price[i]
        if sellOutSignal(i,Min):
            getOut(i,inPrice,True)
    else:
        if buySignal(i,initPrice,initMs):
            getIn(i,True)
        elif sellSignal(i,initPrice,initMs):
            getIn(i,False)
        else:
            if checkTime(i):
                initMs = int(datas[i][0])
                initPrice = price[i]
    
with open(csvname+"_ROI.csv", 'w+', newline='',encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(benefit)