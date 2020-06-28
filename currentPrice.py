from requests import get
import json


def getCurrentPrice(symbol, intradayInterval, priceType, apiKey):
    intradayUrl = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={intradayInterval}&apikey={apiKey}"
    intraday = get(intradayUrl)
    intradayObj = json.loads(intraday.content.decode("utf-8"))
    res = list(intradayObj["Time Series (5min)"])[0]
    currentLowPrice = float(intradayObj["Time Series (5min)"][res][priceType])
    return currentLowPrice
