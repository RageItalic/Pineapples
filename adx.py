from requests import get
import json

def getadx(function, symbol, interval, timePeriod, series, apikey):
    count = 0
    adxcomparator = 0
    adx = 0.0
    apiCALL = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={timePeriod}&series_type={series}&apikey={apikey}"
    adx = get(apiCALL)
    adx1 = json.loads(rsi.content.decode("utf-8"))
    for key, value in adx1.items():
        if key == "Technical Analysis: ADX":
            for adxVAL in value.items():
                if count == 0:
                    adxcomparator = (adxVAL[1])
                    adx = adxcomparator.get('RSI')
                    print(adx)
                    count += 1
    if float(adx) >= 25:
        print("CURRENT TREND IS STRONG")
    else:
        print("CURRENT TREND IS WEAK.")