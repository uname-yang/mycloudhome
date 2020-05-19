import json
import os

import requests

import mycloudhome.configure as configure


def login(username, password):
    token = fetch_token(username, password)
    fetch_user_info(username)
    return token


def fetch_token(username, password):
    url = configure.get('cloud.service.urls', 'service.auth0.url')+'/oauth/ro'
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "openid offline_access",
        "device": "123456789",
        "connection": "Username-Password-Authentication",
        "client_id": "56pjpE1J4c6ZyATz3sYP8cMT47CZd6rk"
    }

    response = requests.post(url, data=payload)
    if configure.debug:
        print(url)
        print(payload)
        print(response.content)
    if response.status_code != 200:
        raise Exception("Login Error !!! [{}][{}]".format(
            response.status_code, response.content))

    token = json.loads(response.content)
    configure.save_token(token)
    return token


def token():
    return configure.get_token()


def fetch_user_info(username):

    url = configure.get('cloud.service.urls', 'service.auth.url') + \
        '/authservice/v2/auth0/user?email={}'
    response = requests.get(url.format(username), headers={
                            'Authorization': 'Bearer '+token()})
    if configure.debug:
        print(url.format(username))
        print(response.content)
    if response.status_code != 200:
        raise Exception("Login Error !!! [{}][{}]".format(
            response.status_code, response.content))

    user_info = json.loads(response.content)

    list(map(lambda user: configure.save_profiles(
        get_list_by_user_id(user['user_id']), user), user_info['data']))

def get_list_by_user_id(user_id):
    url = configure.get('cloud.service.urls',
                        'service.device.url')+'/device/v1/user/{}?pretty=true'
    
    response = requests.get(url.format(user_id), headers={
                            'Authorization': 'Bearer '+ token()})
    if configure.debug:
        print(url.format(user_id))                        
        print(response.content)

    if response.status_code != 200:
        raise Exception("DEVICE INFO Error !!! [{}][{}]".format(
            response.status_code, response.content))

    device_info = json.loads(response.content)
    return device_info['data']