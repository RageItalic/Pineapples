
from requests import get
import json
from currentPrice import getCurrentPrice
import time
from datetime import datetime


def bband(stockHold):
    symbol = "IBM" 
    function = "BBANDS"
    interval = "5min"
    time_period = 10 
    series_type = "close"
    std_dev = 2 
    api_key = "7KQ1O5UFX0KZV6ZP"; 


    #filtering bband data
    bbandUrlCall = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&nbdevup={std_dev}&nbdevdn={std_dev}&apikey={api_key}"
    #bbandUrlCall = "https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=5min&time_period=10&series_type=close&nbdevup=2&nbdevdn=2&apikey=7KQ1O5UFX0KZV6ZP"
    allbbandprice = get(bbandUrlCall)
    bbandObj  = json.loads(allbbandprice.content.decode("utf-8"))
    bbandpriceDict = {}
    count = 0 
    for key, value in bbandObj.items():
        if key == "Technical Analysis: BBANDS":
            for date , bbandpriceDict in value.items():
                print("date", date)
                #if count == 0: 
                #print("hetfhy" ,bbandpriceDict)
                break

    # getting the bband price 
    upper_band = float(bbandpriceDict["Real Upper Band"])
    lower_band = float(bbandpriceDict["Real Lower Band"])
    middle_band = float(bbandpriceDict["Real Middle Band"])
    print(f"Upper_band: {upper_band} \nLower_band: {lower_band} \nMiddle_band : {middle_band}")



    #get the close price for every 5 mins
    currentClosePrice = getCurrentPrice(symbol, interval , "4. close" , api_key)
    prevClosePrice = currentClosePrice
    print(f"Current close price : {currentClosePrice} \nPrevious close price : {prevClosePrice}")

    # stockHold = False
    uptrend = False 
    downtrend = False 
    changingTrend = False

    middle_band_range = 0.0 
    middle_band_range = ((currentClosePrice - middle_band ) / middle_band ) * 100.0

    #trend indicator 
    if currentClosePrice > lower_band and currentClosePrice < middle_band : 
        downtrend = True
        uptrend = False 
        changingTrend = False 
    elif currentClosePrice > middle_band and currentClosePrice < upper_band: 
        uptrend = True 
        downtrend = False 
        changingTrend = False 
    elif middle_band_range < 0.001:
        changingTrend = True 
        uptrend= False 
        downtrend = False 
    else:
        pass
    print(f"Down Trend : {downtrend} \nUp Trend : {uptrend}\nChanged Trend:  {changingTrend}")

    
    
    #downtrend: need to find the double low and then buy 
    if downtrend == True:
        # entry point
        # -----> Here is start my better entry point <-------
        # # if my prev_trend is changed , then I am from a changing point to a downtrend 
        #falls = 0 
        # if falls == 2 and stockHold == True:
        #     print("Buy Now")
        # else:
        #     pass
    
        # # check for my double low 
        # if currentClosePrice < prevClosePrice: 
        #     falls += 1 
        #     prevClosePrice = currentClosePrice 
        # else: 
        #     pass 
        # -----> Here is the end of better entry point  <------

        #lower_band_range is to check that if the current price is touching the band 
        lower_band_range = abs(((currentClosePrice - lower_band) / lower_band ) )

        if lower_band_range < 0.002:
            print("Lower band range:", lower_band_range)
            if stockHold == False:
                print("Buy now")
                print(f"Buy at {currentClosePrice}")
                stockHold = True
                print(f"stock hold: {stockHold}")
            else:
                print("You are holding stock now")
        else: 
            print("not a good time to buy")
            
        

    #uptrend : if the current price is in the range of the upper_band , then sell
    if uptrend == True: 
        upper_band_range = abs(((currentClosePrice - upper_band) / upper_band ) )
        print("Upper band range: " , upper_band_range)
        # if my prev_trend is changed ,then this is from somewhere to a uptrend 
        if upper_band_range < 0.002:  
            if stockHold == True:
                print("Sell Now")
                print(f"sell at {currentClosePrice}")
                stockHold = False
                print(f"stock hold: {stockHold}") 
            else: 
                print("You dont hold any stock")
        else: 
            print("Not in the selling range yet") 
    return stockHold 


    
    # changing point: this is check if we are holding the stock are going to uptrend or donwtrend.
    #if at this point we are still in downtrend , sell the stock 
    # if at this point we are keep going the uptrend , we can keep holding it until we reach the upper band  




def runThis():
    stockHold = False
    totalAmount = 500.0 
    profit = 0.0
    stockOwn = 0.0 

    while True:
        now = datetime.now()
        print(f"now = {now} \n")
        returnResult = bband(stockHold)
        if returnResult == True: 
            stockHold = True 
        else:
            stockHold = False 
        time.sleep(330)


if __name__ == '__main__':
   runThis()