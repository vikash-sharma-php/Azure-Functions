# This is a timer trigger scheduled to run at every 8:50 of monday to friday
# below are the steps in order this timer trigger runs

# 1. check if it is a working day if not holiday
# 2. attempt to login
# 3. dump the picke in storage account

import datetime
import logging
import os
import azure.functions as func
from shared.FyerLogin import login_fyers
from shared.utils import upload_pickle_to_blob
import pickle

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    # if mytimer.past_due:
    #     logging.info('The timer is past due! %s', utc_timestamp)
    try:
        logging.info('Fyers Login Triggered at %s', utc_timestamp)
        fyers_broker = login_fyers()
        if fyers_broker:
            data = pickle.dumps(fyers_broker)
            
            logging.info(data)
            upload_pickle_to_blob(fyers_broker)
    except Exception as e:
        logging.error(e)   

    


