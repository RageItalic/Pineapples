
from requests import get
import json
from currentPrice import getCurrentPrice


def bband():
    symbol = "BF-B" 
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
    print(f"Current close price : {currentClosePrice} \nPrevious close price : {prevClosePrice} \n ")

    stockHold = True 
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

    #save the trend here!! At this point the current trend will become a prev trend when keep getting new data 
    if downtrend == True:
        prev_trend = "downtrend"
    elif uptrend == True:
        prev_trend = "uptrend" 
    elif changingTrend == True: 
        #runn chainging trend function 

    print(f"Down Trend : {downtrend} \nUp Trend : {uptrend}\nChanged Trend:  {changingTrend}")
    
    falls = 0 
    #downtrend: need to find the double low and then buy 
    if downtrend == True:
        print("In the downtrend block")
        # entry point
        if falls == 2 and stockHold == True:
            print("Buy Now")
        else:
            pass
    
        # check for my double low 
        if currentClosePrice < prevClosePrice: 
            falls += 1 
            prevClosePrice = currentClosePrice 
        else: 
            pass 


    #uptrend : if the current price is in the range of the upper_band , then sell
    if uptrend == True: 
        upper_band_range = abs(((currentClosePrice - upper_band) / upper_band ) )
        print("Upper band range: " , upper_band_range)
        if upper_band_range < 0.002:  
            if stockHold == True:
                print("Sell Now")
                stockHold = False 
            else: 
                print("You dont hold any stock")
        else: 
            print("Not in the selling range yet ") 
    

    
# changing point: this is check if we are holding the stock are going to uptrend or donwtrend.
#if at this point we are still in downtrend , sell the stock 
# if at this point we are keep going the uptrend , we can keep holding it until we reach the upper band  
# this chaning trend function will tell us that if it is a   
#def changingTrend(prev_trend, stockHold, )


# def runThis():
#     downtrend = bband() #true or false
#     falls = 0
#     while (True):
#         bband()




    


if __name__ == '__main__':
   bband()