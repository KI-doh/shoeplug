import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

# SAFARICOM SANDBOX CREDENTIALS

CONSUMER_KEY = "uP4lUeh6eyGXTaPWeAHXTw8IyXzDJ2YIGMaLyN7DVecQ9JOq"

CONSUMER_SECRET = "lrRMm22OeFJRgYADTkejDeC15KC8b3vpqi61RQ82QLVelwLgcDtTKOrEaa423pJl"

BUSINESS_SHORT_CODE = "174379"

PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

CALLBACK_URL = "https://abacus-joyous-hurricane.ngrok-free.dev/mpesa-callback/"


def get_access_token():

    url = (
        "https://sandbox.safaricom.co.ke/"
        "oauth/v1/generate?grant_type=client_credentials"
    )

    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            CONSUMER_KEY,
            CONSUMER_SECRET
        )
    )

    return response.json().get("access_token")


def stk_push(phone_number, amount):

    access_token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        (
            BUSINESS_SHORT_CODE +
            PASSKEY +
            timestamp
        ).encode()
    ).decode()

    url = (
        "https://sandbox.safaricom.co.ke/"
        "mpesa/stkpush/v1/processrequest"
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORT_CODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "ShoePlug",
        "TransactionDesc": "Shoe Purchase"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print("SAFARICOM RESPONSE:")
    print(response.text)

    return response.json()