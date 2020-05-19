import json
import os
from pathlib import Path

import requests

import mycloudhome.configure as configure
import mycloudhome.auth as auth

from collections import OrderedDict
from pprint import pformat


def load_json_preserve_order(s):
    return json.loads(s, object_pairs_hook=OrderedDict)


def pretty(d: dict):
    return pformat(d)


# wd:// --> root
# wd://temp/a.txt --> some file id
def convert_wd_path_to_wd_id(wdPath):
    if wdPath == 'wd://' or wdPath == 'root':
        return 'root'
    idx = 'root'
    for name in wdPath.replace("wd://", "").split('/'):
        if name == "":
            continue
        sub_dir = get_file_under_dir_by_name(name, idx)
        if sub_dir is None:
            raise Exception("WD PATH Not FOUND!!! [{}]".format(name))
        idx = sub_dir['id']

    if configure.debug:
        print("Convert {} to {}".format(wdPath, idx))
    return idx

def get_file_under_dir_by_name(name, dir_id, pagetoken=""):
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/filesSearch/parents?ids={}&limit=100&order=desc&orderBy=name&pretty=true&pageToken={}'

    response = requests.get(url.format(dir_id, pagetoken), headers={
                            'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print("search {} in parents {}".format(name, dir_id))
        print(url.format(dir_id, pagetoken))
        print(response.content)

    if response.status_code != 200:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))

    data = json.loads(response.content)

    if 'files' in data:
        for item in data['files']:
            if item['name'] == name:
                return item
        if data['pageToken'] != "":
            return get_file_under_dir_by_name(name, dir_id, data['pageToken'])

    return None

def is_wd_path(path):
    if path.startswith('wd://'):
        return True
    if path == 'root':
        return True
    return False


def is_local_dir(path):
    return Path(path).is_dir()

def is_local_file(path):
    return Path(path).is_file()

def get_local_file_name(path):
    return Path(path).name