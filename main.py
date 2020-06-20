import time
from requests import get
from multiprocessing import Process
from dotenv import load_dotenv
import json
import os
from priceCrossover import priceCrossover

load_dotenv()



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

    for symbol in symbols:
        Process(
            target=priceCrossover,
            args=(
                symbol,
                intradayInterval,
                function,
                interval,
                timePeriod,
                apiKey,
                userData,
                stopLoss,
                takeProfit,
            ),
        ).start()
        print(userData)
        print("\n")


runStrategies()
