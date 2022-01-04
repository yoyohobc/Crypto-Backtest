import numpy as np
import talib,csv
#技術指標跑回測
#幣種＆初始金額
crypto = 'ETH'
usd = 725
beginDay = 100
beginIndex = beginDay * 1440
csvname = crypto+"_1m"
with open(csvname+".csv", newline='',encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    price = list(rows)
price = [float(p[0]) for p in price]
print("start...")
def calculator(index,kRange):
    if kRange == '1day':
        per = 1440
    elif kRange == '1hr':
        per = 60
    elif kRange == '15min':
        per = 15
    else:
        per = 5
    close = np.array([float(price[k]) for k in range(index-(per*beginDay),index,per)])
    '''ema12 = talib.EMA(close,12)
    ema26 = talib.EMA(close,26)
    dif = np.array([float(ema12[i] - ema26[i]) for i in range(len(ema12))])
    dem = talib.EMA(dif,9)
    return dif,dem
    rsi2 = talib.RSI(close,5)
    rsi12 = talib.RSI(close,10)'''
    macd = talib.MACD(close)
    return macd

def upSignal(index,kRange):
    macd = calculator(index,kRange)
    return macd > 0

def downSignal(index,kRange):
    macd = calculator(index,kRange)
    return macd <= 0
def buySignal(index):
    '''fiveMin = upSignal(index,'5min')
    fifteenMin = upSignal(index,'15min')
    anHour = upSignal(index,'1hr')
    aDay = upSignal(index,'1day')
    return fiveMin and fifteenMin and anHour and aDay'''
    return upSignal(index,'1day')

def sellSignal(index):
    return downSignal(index,'1day')

def daysCount(index):
    return str((index - beginIndex)//1440) + " days"
buy = False
buyPrice = 0
benefit = []
#total = 0
for i in range(beginIndex,len(price)):
    if not buy:
        if buySignal(i):
            buy = True
            buyPrice = price[i]
            day = daysCount(i)
            benefit.append(['buy',price[i],usd,day])
    else:
        percent = price[i]/buyPrice
        #if(percent >= 1.01 or sellSignal(i)):
        if(sellSignal(i)):
            #usd += (percent-1)*usd*1
            usd *= percent
            day = daysCount(i)
            benefit.append(['sell',price[i],usd,day])
            buy = False
        #elif(percent <= 0.9 or usd <= 10):
        elif(usd <= 10):
            day = daysCount(i)
            benefit.append(['sell',price[i],0,day])
            break
with open(crypto+'_benefit.csv', 'w+', newline='',encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(benefit)