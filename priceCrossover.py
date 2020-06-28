from currentPrice import getCurrentPrice
from sma import getSMA
from trackAndTrade import trackAndTrade
from sendSMS import sendSMS
import time


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
    currentLowPrice = getCurrentPrice(symbol, intradayInterval, "3. low", apiKey)
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
