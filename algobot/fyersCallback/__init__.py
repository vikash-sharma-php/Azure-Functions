import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    auth_code = req.params.get('auth_code')
    status = req.params.get('s')
    code = req.params.get('code')
    logging.info(f"s={status}; code={code}; auth_code={auth_code}")
    return func.HttpResponse(f"{auth_code}")
