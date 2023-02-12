import logging
from pyotp import TOTP
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )



def main(req: func.HttpRequest) -> func.HttpResponse:
    ZERODHA_TOTP_KEY = 'KEDCSYPWRF74NRHKXSRLAJCI7O2FGG5D'
    totp = TOTP(ZERODHA_TOTP_KEY)
    return func.HttpResponse(totp.now())