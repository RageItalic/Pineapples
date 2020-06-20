import time
from requests import get
from multiprocessing import Process
from twilio.rest import Client
from dotenv import load_dotenv
import json
import os

load_dotenv()


def sendSMS(action, symbol, price, extraMsg):
    account_sid = os.environ.get("twilioAccountSID")
    auth_token = os.environ.get("twilioAccountAuthToken")
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f"{action} {symbol} at {price} now!! \n{extraMsg}",
        from_="+17816510732",
        to="+14372197106",
    )


def getCurrentLowPrice(symbol, intradayInterval, apiKey):
    intradayUrl = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={intradayInterval}&apikey={apiKey}"
    intraday = get(intradayUrl)
    intradayObj = json.loads(intraday.content.decode("utf-8"))
    res = list(intradayObj["Time Series (5min)"])[0]
    currentLowPrice = float(intradayObj["Time Series (5min)"][res]["3. low"])
    return currentLowPrice


def trackAndTrade(
    symbol,
    userData,
    stopLoss,
    takeProfit,
    intradayInterval,
    apiKey,
    initialCurrentLowPrice,
):
    count = 0
    while True:
        currentLowPrice = 0
        if count > 0:
            currentLowPrice = getCurrentLowPrice(symbol, intradayInterval, apiKey)
        else:
            currentLowPrice = initialCurrentLowPrice
            count += 1
        currentAmountInStock = userData[symbol]["totalShares"] * currentLowPrice
        print("UPDATED current low price!!!!!!", currentLowPrice)
        print(
            "THIS IS HOW MUCH YOU ORIGINALLY INVESTED:",
            userData[symbol]["amountInvested"],
        )
        print("this is the amount currently in the stock:", currentAmountInStock)
        percentageChange = float(
            currentAmountInStock / userData[symbol]["amountInvested"]
        )
        # stop condition here
        if percentageChange <= 0.99:
            print("We are at a loss of one percent or more. TIME TO SELL. (AT LOSS)")
            print("Simulate sell here...")
            print("then break out of loop because you have sold your shares.")
            print(f"NOTHING to track anymore for {symbol}")
            sendSMS(
                "SELL",
                symbol,
                currentLowPrice,
                "Stock price is dropping, sell quick while loss is still 1%.",
            )
            break
        elif percentageChange >= 1.02:
            print(
                "We are at a profit of TWO (or more!) percent. TIME TO SELL. (AT PROFIT)"
            )
            print("Simulate sell here...")
            print("then break out of loop because you have sold your shares.")
            print(f"NOTHING to track anymore for {symbol}")
            sendSMS(
                "SELL",
                symbol,
                currentLowPrice,
                "Stock price is rising, sell quick while profit is still 2%.",
            )
            break

        print(f"NOTHING SPECIAL HAPPENED BRO. Percent change is {percentageChange}")
        time.sleep(330)


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


def priceCrossover(
    symbol,
    intradayInterval,
    function,
    interval,
    timePeriod,
    apiKey,
    userData,
    stopLoss,
    takeProfit,
):
    currentLowPrice = getCurrentLowPrice(symbol, intradayInterval, apiKey)
    print(
        "Checking to see if current low price is higher than last weeks average to ensure rising price..."
    )
    print("Current low price", currentLowPrice)
    latestWeekAvg = getSMA(function, symbol, interval, timePeriod, "open", apiKey)
    print("Average over last week", latestWeekAvg)

    if currentLowPrice > latestWeekAvg:
        print(f"invest in {symbol} right now.")
        print("SIMULATING BUY...")
        # simulate buy here
        # basically,
        # update userData[totalCash] and subtract from it moneyAvailable in userData[symbol]
        # then, in userData[symbol]["amountInvested"] = userData[symbol]["moneyAvailable"],
        # set userData[symbol][moneyAvailable] = 0 because you have no more money available
        # set bought at to be current low price,
        # totalShares = amountInvested/boughtAt
        # set buyTime to current time
        # then, trigger an actual tracker function here that accepts symbol, userData, stopLoss and takeProfit
        # that runs every 5 minutes to see if current price == boughtAt * takeProfit
        # if true, simulate sell (for profit)
        # else if current price == (boughtAt - boughtAt * stopLoss)
        # then simulate sell (for loss)
        sendSMS("BUY", symbol, currentLowPrice, "Stock price seems to be rising.")
        userData["totalCash"] -= userData[symbol]["moneyAvailable"]
        userData[symbol]["amountInvested"] = userData[symbol]["moneyAvailable"]
        userData[symbol]["moneyAvailable"] = 0
        userData[symbol]["boughtAt"] = currentLowPrice
        userData[symbol]["totalShares"] = (
            userData[symbol]["amountInvested"] / userData[symbol]["boughtAt"]
        )
        userData[symbol]["buyTime"] = time.strftime("%D, %H:%M:%S", time.localtime())

        trackAndTrade(
            symbol,
            userData,
            stopLoss,
            takeProfit,
            intradayInterval,
            apiKey,
            currentLowPrice,
        )
    else:
        print(
            f"Dont buy {symbol}... or if you have it, then sell!! This part still needs to be built out."
        )
    return 1


def runStrategies():
    symbols = ["M", "AAL"]
    apiKey = os.environ.get("alphaVantageApiKey")
    function = "SMA"
    interval = "daily"
    timePeriod = "10"
    intradayInterval = "5min"
    stopLoss = 0.01
    takeProfit = 1.02
    totalCash = 1000

    userData = {
        "totalCash": totalCash,
        "M": {
            "moneyAvailable": totalCash / 2,
            "totalShares": 0,
            "amountInvested": 0,
            "boughtAt": 0,
            "buyTime": None,
            "soldAt": 0,
            "sellTime": None,
            "amountMade": 0,
        },
        "AAL": {
            "moneyAvailable": totalCash / 2,
            "totalShares": 0,
            "amountInvested": 0,
            "boughtAt": 0,
            "buyTime": None,
            "soldAt": 0,
            "sellTime": None,
            "amountMade": 0,
        },
    }

    # for symbol in symbols:
    #     Process(
    #         target=priceCrossover,
    #         args=(
    #             symbol,
    #             intradayInterval,
    #             function,
    #             interval,
    #             timePeriod,
    #             apiKey,
    #             userData,
    #             stopLoss,
    #             takeProfit,
    #         ),
    #     ).start()
    #     print(userData)
    #     print("\n")


runStrategies()
