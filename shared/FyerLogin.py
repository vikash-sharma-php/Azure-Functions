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
import base64
# from os.path import isfile
from config import config

import logging

# fyers.get_profile()
# fyers.funds()


def login_fyers_old():

    user_id = "XP--------"
    password = "------------"
    pin = "----"
    client_id = "----------"
    app_id = client_id[:-4]
    secret_key = "----------"
    redirect_uri = "http://localhost:5000"
    response_type = "code"
    grant_type = "authorization_code"
    state = "abcd1243"
    scope = ""
    nonce = ""

    today_str = date.strftime(date.today(), '%d_%m_%Y')
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
    r3 = s.post("https://api.fyers.in/api/v2/token",
                headers=headers, data=data3)

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
        # (By default the async will be False, Change to True for async API calls.)
        False
    )

    log_path = "logs/"

    fyers = fyersModel.FyersModel(
        client_id=client_id, token=access_token, is_async=is_async, log_path=log_path
    )

    # with open(fyer_pickle_file_name, "wb") as f:
    #     pickle.dump(fyers, f)

    return fyers


logging.getLogger(__name__)


def login_fyers():
    if config.config_data is None:
        logging.error(
            f'unable to load the config data. cannot login to fyers.')
        return

    user_id = config.fyers_api.user_id
    password = config.fyers_api.password
    app_id = config.fyers_api.client_id[:-4]

    today_str = date.strftime(date.today(), '%d_%m_%Y')
    # fyer_pickle_file_name = "res/fyers_{0}.pickle".format(today_str)
    # access_token_file_name = "res/fyers_access_token_{0}.txt".format(today_str)

    # if isfile(fyer_pickle_file_name) and isfile(access_token_file_name):
    #     with open(fyer_pickle_file_name,'rb') as f:
    #         fyers = pickle.load(f)
    #     return fyers

    session = accessToken.SessionModel(
        client_id=config.fyers_api.client_id,
        secret_key=config.fyers_api.secret_key,
        redirect_uri=config.fyers_api.redirect_uri,
        response_type=config.fyers_api.response_type,
        grant_type=config.fyers_api.grant_type,
        state=config.fyers_api.state,
        scope=config.fyers_api.scope,
        nonce=config.fyers_api.nonce,
    )

    # with open("access_token.txt", "r") as f:
    #     access_token = f.read()
    s = Session()

    API_ENDPOINT = "https://api-t2.fyers.in/vagator/v2/"
    send_login_otp_v2 = API_ENDPOINT + "send_login_otp_v2"
    verify_otp = API_ENDPOINT + "verify_otp"
    verify_pin_v2 = API_ENDPOINT + "verify_pin_v2"
    token = 'https://api.fyers.in/api/v2/token'
    totp_url = "https://algobot.azurewebsites.net/api/totp?code=FjEZlPGaDvd1mHEnKCyN2naXfIec3jDSpkLkT1SpHQCZAzFudyAy8g==&broker=fyers"

    headers = {
        "Cache-Control":  "max-age=0",
        "Sec-Fetch-Mode":  "navigate",
        "Accept-Language":  "en-US,en;q=0.9",
        "sec-ch-ua":  "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "Accept-Encoding":  "gzip, deflate, br",
        "sec-ch-ua-platform":  "\"Windows\"",
        "Accept":  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "DNT":  "1",
        "sec-ch-ua-mobile":  "?0",
        "Sec-Fetch-Site":  "none",
        "Sec-Fetch-Dest":  "document",
        "Sec-Fetch-User":  "?1",
        "Upgrade-Insecure-Requests":  "1"
    }

    # send login otp v2
    body = {
        'fy_id': base64.b64encode(bytes(config.fyers_api.user_id, 'utf-8')).decode('utf-8'),
        'app_id': '2'
    }
    res_send_login_otp_v2 = s.post(
        url=send_login_otp_v2, headers=headers, json=body)
    res_send_login_otp_v2.json()
    request_key = res_send_login_otp_v2.json()['request_key']

    # verify otp
    totp = s.get(totp_url).content.decode('utf-8')
    body = {
        'request_key': request_key,
        "otp": totp
    }
    res_verify_otp = s.post(url=verify_otp, headers=headers, json=body)
    request_key = res_verify_otp.json()['request_key']

    # verify pin
    body = {
        "request_key": request_key,
        "identity_type": "pin",
        "identifier": base64.b64encode(bytes(config.fyers_api.pin, 'utf-8')).decode('utf-8')
    }
    res_verify_pin_v2 = s.post(url=verify_pin_v2, headers=headers, json=body)
    res_verify_pin_v2.json()

    # Generate token
    # s.cookies.set_cookie()
    body = {
        "fyers_id": config.fyers_api.user_id,
        "password": config.fyers_api.password,
        "pan_dob": "----------",
        "app_id": app_id,
        "redirect_uri": "--------------------------------",
        "appType": "100",
        "code_challenge": "",
        "state": "None",
        "scope": "",
        "nonce": "",
        "response_type": "code",
        "create_cookie": True
    }
    bearer_token = res_verify_pin_v2.json()['data']['access_token']
    headers["Authorization"] = f"Bearer {bearer_token}"
    res_token = s.post(url=token, headers=headers, json=body)
    res_token.json()

    Url = res_token.json()['Url']
    parsed = urlparse(Url)
    auth_code = parse_qs(parsed.query)["auth_code"][0]

    session.set_token(auth_code)
    res = session.generate_token()

    access_token = res["access_token"]

    # print('access token: ', access_token)
    # with open(access_token_file_name, "w") as f:
    #     f.write(access_token)

    # (By default the async will be False, Change to True for async API calls.)
    is_async = False

    log_path = "logs/"

    fyers = fyersModel.FyersModel(
        client_id=config.fyers_api.client_id, token=access_token, is_async=is_async, log_path=log_path
    )

    # with open(fyer_pickle_file_name, "wb") as f:
    #     pickle.dump(fyers, f)

    return fyers


def get_fyers_broker_handle(config, access_token):
    # (By default the async will be False, Change to True for async API calls.)
    is_async = False
    log_path = "logs/"

    fyers = fyersModel.FyersModel(
        client_id=config.fyers_api.client_id, token=access_token, is_async=is_async, log_path=log_path
    )

    return fyers


class FyersHandler:
    def __init__(self):
        self._brokerHandle = None
        self._accessToken = None

    def get_access_token():
        """ tries to login to fyers and gets access token."""
        pass
    


fyers = login_fyers()
