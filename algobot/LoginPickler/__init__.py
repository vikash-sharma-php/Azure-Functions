# This is a timer trigger scheduled to run at every 8:50 of monday to friday
# below are the steps in order this timer trigger runs

# 1. check if it is a working day if not holiday
# 2. attempt to login
# 3. dump the picke in storage account

import datetime
import logging

import azure.functions as func
from shared.FyerLogin import login_fyers
from shared.utils import upload_pickle_to_blob


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due! %s', utc_timestamp)

    logging.info('Fyers Login Triggered at %s', utc_timestamp)
    fyers_broker = login_fyers()
    if fyers_broker:
        upload_pickle_to_blob(fyers_broker)
    

    


