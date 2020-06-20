from requests import get
import json


def getSMA(function, symbol, interval, timePeriod, series, apikey):
    apiCall = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={timePeriod}&series_type={series}&apikey={apikey}"
    response = get(apiCall)
    quote = json.loads(response.content.decode("utf-8"))
    count = 0
    sum = 0.0
    # latestWeekAvg = 0.0
    priceCrossoverArray = []
    for key, value in quote.items():
        # print(key, value)
        if key == "Technical Analysis: SMA":
            for date, smaVal in value.items():
                if count < 7:
                    priceCrossoverArray.append(smaVal)
                    # print(date, ' : ', smaVal)
                    count += 1

    for avgDay in priceCrossoverArray:
        sum += float(avgDay["SMA"])
    latestWeekAvg = sum / 7
    return latestWeekAvg
