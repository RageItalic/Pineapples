import time
from sendSMS import sendSMS
from currentLowPrice import getCurrentLowPrice


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
