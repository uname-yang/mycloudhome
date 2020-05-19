import json
import os

import requests

import mycloudhome.configure as configure
import mycloudhome.auth as auth
import mycloudhome.utils as utils

from pprint import pformat

def get_list_by_user_id(user_id):
    return auth.get_list_by_user_id(user_id)


def get_by_device_id(device_id):
    url = configure.get('cloud.service.urls',
                        'service.device.url')+'/device/v1/device/{}?pretty=true'
    
    response = requests.get(url.format(device_id), headers={
                            'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url.format(device_id))
        print(response.content)

    if response.status_code != 200:
        raise Exception("DEVICE INFO Error !!! [{}][{}]".format(
            response.status_code, response.content))

    device_info = json.loads(response.content)
    return device_info['data']


def get_user_list_by_device_id(device_id):
    url = configure.get('cloud.service.urls',
                        'service.device.url')+'/device/v1/device/{}/user?pretty=true'

    response = requests.get(url.format(device_id), headers={
                            'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url.format(device_id))
        print(response.content)
        
    if response.status_code != 200:
        raise Exception("DEVICE INFO Error !!! [{}][{}]".format(
            response.status_code, response.content))

    device_info = json.loads(response.content)
    return device_info['data']
