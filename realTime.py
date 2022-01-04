from binance.client import Client
from datetime import datetime as dt
from config import *
import numpy as np
import matplotlib.pyplot as plt
import talib
#輸入幣種和計算區間
crypto = 'ETH'
calculateRange = '1hr'
#1day,1hr,15min,5min
client = Client(api_key, api_secret)
def calculate(product,kRange):
    if kRange == '1day':
        kline = Client.KLINE_INTERVAL_1DAY
        strRange = "300 day ago UTC"
    elif kRange == '1hr':
        kline = Client.KLINE_INTERVAL_1HOUR
        strRange = "15 day ago UTC"
    elif kRange == '15min':
        kline = Client.KLINE_INTERVAL_15MINUTE
        strRange = "5 day ago UTC"
    else:
        kline = Client.KLINE_INTERVAL_5MINUTE
        strRange = "3 day ago UTC"
    candles = client.get_historical_klines(product, kline, strRange)
    dateList = [str(dt.fromtimestamp(int(c[0])/1000)) for c in candles]
    high = np.array([float(c[2]) for c in candles])
    low = np.array([float(c[3]) for c in candles])
    close = np.array([float(c[4]) for c in candles])
    ema5 = talib.EMA(close,5)
    ema10 = talib.EMA(close,10)
    ema20 = talib.EMA(close,20)
    ema12 = talib.EMA(close,12)
    ema26 = talib.EMA(close,26)
    dif = np.array([float(ema12[i] - ema26[i]) for i in range(len(ema12))])
    dem = talib.EMA(dif,9)
    macd = talib.MACD(close)
    rsi6 = talib.RSI(close,6)
    k, d = talib.STOCH(high=high,low=low,close=close,fastk_period=9,slowk_period=3,slowd_period=3)
    print("DEM",dem[-1])
    print("DIF",dif[-1])
    print("MACD",macd[-1][-1])
    print("EMA(5)",ema5[-1])
    print("EMA(10)",ema10[-1])
    print("EMA(20)",ema20[-1])
    print("RSI(6)",rsi6[-1])
    print("K",k[-1])
    print("D",d[-1])
    print("當前價",candles[-1][4],"USDT")
    print("計算時間",dateList[-1])
    num = 24
    days = [d[11:13] for d in dateList[-num:]]
    plt.plot(days,k[-num:], color=(255/255,100/255,100/255))
    plt.plot(days,d[-num:], color=(100/255,100/255,255/255))
    plt.title("KD graph") # title
    plt.ylabel("KD")
    plt.xlabel("time")
    plt.grid(True)
    plt.show()

calculate(crypto+'USDT',calculateRange)