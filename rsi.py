from requests import get
import json

def getrsi():
    count = 0
    rsicomparator = 0
    rsi = 0.0
    apiCALL = f"https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=15min&time_period=10&series_type=open&apikey=7KQ1O5UFX0KZV6ZP"
    rsi = get(apiCALL)
    rsi1 = json.loads(rsi.content.decode("utf-8"))
    for key, value in rsi1.items():
        if key == "Technical Analysis: RSI":
            for rsiVAL in value.items():
                if count == 0:
                    rsicomparator = (rsiVAL[1])
                    rsi = rsicomparator.get('RSI')
                    print(rsi)
                    count += 1
    if float(rsi) >= 70:
        print("RSI INDEX IS OVER 70.. NOT THE BEST TIME TO INVEST")
    elif float(rsi) <= 30:
        print("RSI INDEX IS UNDER 30.. GOOD TIME TO INVEST")
    else:
        print("RSI INDEX IS BETWEEN 30 AND 70.. SEE ANOTHER INDICATOR FOR MORE INFO ON THE TRENDS.")


    #call rsi from API
    #check if rsi is above 70 or below 30p
    #if rsi is below 30, buying is a good idea and if it's above 70 selling is the goto
    #so if these values are true, then we check with the other indicators and see their trends to  confirm with the trends of the RSI


getrsi()


