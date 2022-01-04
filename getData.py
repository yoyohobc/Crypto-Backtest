from binance.client import Client
from config import *
import csv
#取得過去資料
#幣種＆時間間隔
crypto = "ETH"
calculatePeriod = '1d'
#KLINE_INTERVAL_1MINUTE = '1m'
#KLINE_INTERVAL_3MINUTE = '3m'
#KLINE_INTERVAL_5MINUTE = '5m'
#KLINE_INTERVAL_15MINUTE = '15m'
#KLINE_INTERVAL_30MINUTE = '30m'
#KLINE_INTERVAL_1HOUR = '1h'
#KLINE_INTERVAL_2HOUR = '2h'
#KLINE_INTERVAL_4HOUR = '4h'
#KLINE_INTERVAL_6HOUR = '6h'
#KLINE_INTERVAL_8HOUR = '8h'
#KLINE_INTERVAL_12HOUR = '12h'
#KLINE_INTERVAL_1DAY = '1d'
#KLINE_INTERVAL_3DAY = '3d'
#KLINE_INTERVAL_1WEEK = '1w'
#KLINE_INTERVAL_1MONTH = '1M'
csvname = crypto+"_"+calculatePeriod+".csv"
client = Client(api_key, api_secret)
candles = client.get_historical_klines(crypto+'USDT', calculatePeriod, "1 Jan, 2017")
close = [c for c in candles]
with open(csvname, 'w+', newline='',encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(close)