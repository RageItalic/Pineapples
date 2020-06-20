from twilio.rest import Client
import os


def sendSMS(action, symbol, price, extraMsg):
    account_sid = os.environ.get("twilioAccountSID")
    auth_token = os.environ.get("twilioAccountAuthToken")
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f"{action} {symbol} at {price} now!! \n{extraMsg}",
        from_="+17816510732",
        to="+14372197106",
    )

    print("Message Sent!")
    return 1
