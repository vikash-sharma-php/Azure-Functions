# INSTALLATION:
# pip install fyers-apiv2

# import pickle
from fyers_api import accessToken
# AUTHORIZATION:
from fyers_api import fyersModel
from requests import Session
# import requests
from urllib.parse import urlparse, parse_qs
from datetime import date

# from os.path import isfile


# fyers.get_profile()
# fyers.funds()

def login_fyers():

    user_id = "XP21688"
    password = "AfterEarth@1"
    pin = "1243"
    client_id = "BM0GOPQOYK-100"
    app_id = client_id[:-4]
    secret_key = "5VOWZHXO86"
    redirect_uri = "https://algobot.azurewebsites.net/api/"
    response_type = "code"
    grant_type = "authorization_code"
    state = "abcd1243"
    scope = ""
    nonce = ""


    today_str = date.strftime(date.today(),'%d_%m_%Y')
    fyer_pickle_file_name = "res/fyers_{0}.pickle".format(today_str)
    access_token_file_name = "res/fyers_access_token_{0}.txt".format(today_str)

    # if isfile(fyer_pickle_file_name) and isfile(access_token_file_name):
    #     with open(fyer_pickle_file_name,'rb') as f:
    #         fyers = pickle.load(f)
    #     return fyers

    session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type,
        state=state,
        scope=scope,
        nonce=nonce,
    )

    # with open("access_token.txt", "r") as f:
    #     access_token = f.read()
    s = Session()

    try:
        data1 = f'{{"fy_id":"{user_id}","password":"{password}","app_id":"2","imei":"","recaptcha_token":""}}'
        r1 = s.post("https://api.fyers.in/vagator/v1/login", data=data1)
        if r1.status_code == 200:
            request_key = r1.json()["request_key"]
        else:
            print(r1.json())
    except Exception as e:
        print(e)
        

    data2 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{pin}","recaptcha_token":""}}'
    r2 = s.post("https://api.fyers.in/vagator/v1/verify_pin", data=data2)

    headers = {
        "authorization": f"Bearer {r2.json()['data']['access_token']}",
        "content-type": "application/json; charset=UTF-8",
    }

    data3 = f'{{"fyers_id":"{user_id}","app_id":"{app_id}","redirect_uri":"{redirect_uri}","appType":"100","code_challenge":"","state":"{state}","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
    r3 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data3)


    parsed = urlparse(r3.json()["Url"])
    auth_code = parse_qs(parsed.query)["auth_code"][0]
    # print('auth_code:', auth_code)

    # response = session.generate_authcode()
    # auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NTkzODE3MDYsImV4cCI6MTY1OTQxMTcwNiwibmJmIjoxNjU5MzgxMTA2LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYUDIxNjg4Iiwibm9uY2UiOiIiLCJhcHBfaWQiOiJCTTBHT1BRT1lLIiwidXVpZCI6ImU1MGE0ZGI2ZDc2OTRlOTc5OGVhZDIzNTJmYWE2NjAxIiwiaXBBZGRyIjoiMC4wLjAuMCIsInNjb3BlIjoiIn0.8DYniCW0iJuk4aWY1a9o7pf4Z2txF9mmPWZoIOnhOJ4"

    session.set_token(auth_code)
    res = session.generate_token()

    access_token = res["access_token"]

    # print('access token: ', access_token)
    # with open(access_token_file_name, "w") as f:
    #     f.write(access_token)

    is_async = (
        False  # (By default the async will be False, Change to True for async API calls.)
    )

    log_path = "logs/"

    fyers = fyersModel.FyersModel(
        client_id=client_id, token=access_token, is_async=is_async, log_path=log_path
    )
    
    # with open(fyer_pickle_file_name, "wb") as f:
    #     pickle.dump(fyers, f)

    return fyers
