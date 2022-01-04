# 加密貨幣交易策略回測
利用幣安API抓取貨幣歷史資料,並使用不同交易策略、技術指標做獲利回測,目前仍在測試中

## Installation
pip install -r requirements.txt

```bash
pip install python-binance
pip install TA-Lib
pip install numpy
pip install matplotlib
```

## Usage
config.py
```python
api_key = 'your binance api key'
api_secret = 'your binance secret key'
```
取得特定幣的歷史資料並匯出csv
getData.py
```python
#取得過去資料
#幣種＆時間間隔
crypto = "ETH"
calculatePeriod = '1d'
```
取得即時資料指標
realTime.py
```python
#輸入幣種和計算區間
crypto = 'ETH'
calculateRange = '1hr'
#1day,1hr,15min,5min
```
特定時間突破區間追價策略&技術指標跑回測
backTest.py & backTestTAI.py
```python
#幣種＆初始金額
crypto = 'ETH'
usd = 725
```
