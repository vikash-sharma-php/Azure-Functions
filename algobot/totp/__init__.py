import logging
from pyotp import TOTP
import azure.functions as func
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    brokerName = req.params.get("broker")
    if brokerName is None:
        return func.HttpResponse(body="bad request. specify broker name.", status_code=400)
    logging.info(f"brokerName : {brokerName}")

    if brokerName.lower() == "zerodha":
        KEY = os.getenv("ZERODHA_TOTP_KEY")
    elif brokerName.lower() == "fyers":
        KEY = os.getenv("FYERS_TOTP_KEY")
    else:
        return func.HttpResponse(
            body=f"bad request. broker Name {brokerName} no configured", status_code=400
        )

    logging.info(f'TOTP key : {KEY}')

    if KEY is None:
        return func.HttpResponse("Unknown Error",status_code=500)

    totp = TOTP(KEY)
    return func.HttpResponse(totp.now())
