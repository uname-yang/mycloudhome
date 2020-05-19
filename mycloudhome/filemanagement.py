import json
import os

import requests
from progress.bar import Bar

import mycloudhome.configure as configure
import mycloudhome.auth as auth
import mycloudhome.utils as utils


def get_file_list(wdUri, pagetoken=""):
    if not utils.is_wd_path(wdUri):
        raise Exception("Not WD PATH !!!")
    dir_id = utils.convert_wd_path_to_wd_id(wdUri)
    info = get_file_by_id(dir_id)
    if info['mimeType'] == "application/x.wd.dir":
        return get_file_list_by_id(dir_id, pagetoken)
    else:
        return info


def get_file_list_by_id(wdUri, pagetoken=""):
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/filesSearch/parents?ids={}&limit=100&order=desc&orderBy=name&pretty=true&pageToken={}'

    response = requests.get(url.format(wdUri, pagetoken), headers={
                            'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url.format(wdUri, pagetoken))
        print(response.content)

    if response.status_code != 200:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))

    file_info = json.loads(response.content)
    return file_info


def get_file_by_id(file_id):
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/files/{}?pretty=true'

    response = requests.get(url.format(file_id), headers={
                            'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url.format(file_id))
        print(response.content)

    if response.status_code != 200:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))

    file_info = json.loads(response.content)
    return file_info


def move(src, dst):
    src_id = utils.convert_wd_path_to_wd_id(src)
    dst_id = utils.convert_wd_path_to_wd_id(dst)

    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/files/{}/patch'.format(src_id)
    payload = {"parentID": dst_id}

    response = requests.post(url, data=json.dumps(payload), headers={
                             "Content-Type": "application/json", 'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url)
        print(payload)
        print(response.content)
    if response.status_code != 204:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))


def delete(wdUri):
    file_id = utils.convert_wd_path_to_wd_id(wdUri)
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/files/{}'.format(file_id)

    response = requests.delete(url, headers={
                               "Content-Type": "application/json", 'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url)
        print(response.content)
    if response.status_code in [200, 202, 204]:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))


def rename(wdUri, name):
    file_id = utils.convert_wd_path_to_wd_id(wdUri)
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v2/files/{}/patch'.format(file_id)
    payload = {"name": name}

    response = requests.post(url, data=json.dumps(payload), headers={
                             "Content-Type": "application/json", 'Authorization': 'Bearer '+auth.token()})
    if configure.debug:
        print(url)
        print(payload)
        print(response.content)
    if response.status_code != 204:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))


def download(wdUri, localPath):
    file_id = utils.convert_wd_path_to_wd_id(wdUri)
    url = configure.get(configure.get_default_profile(), 'externaluri') + \
        '/sdk/v3/files/{}/content'.format(file_id)

    response = requests.get(url,
                            headers={"Content-Type": "application/json",
                                     'Authorization': 'Bearer '+auth.token()},
                            stream=True
                            )

    fileName = os.path.join(localPath, get_file_by_id(file_id)['name'])
    if configure.debug:
        print(url)
        print(fileName)

    if response.status_code != 200:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))

    progress = Bar('Downloading', max=get_file_by_id(
        file_id)['size'], suffix='%(percent)d%%')

    with open(fileName, 'wb') as file_handler:
        for chunk in response.iter_content(1024):
            file_handler.write(chunk)
            progress.next(1024)
        progress.finish()


def mkdir(wdUri):
    idx = 'root'
    for name in wdUri.replace("wd://", "").split('/'):
        if name == "":
            continue

        sub_dir = utils.get_file_under_dir_by_name(name, idx)
        if sub_dir is None:
            create_floder(name, idx)
            continue

        if sub_dir['mimeType'] != "application/x.wd.dir":
            raise Exception("WD PATH IS NOT DIR!!! [{}]".format(name))

        idx = sub_dir['id']


def create_floder(name, parentID):
    url = configure.get(configure.get_default_profile(),
                        'externaluri') + '/sdk/v2/files?resolveNameConflict=1'

    payload = """
--xxoo1707a7a80f1xxoo

{{"name":"{}","parentID":"{}","mimeType":"application/x.wd.dir"}}
--xxoo1707a7a80f1xxoo--
""".format(name, parentID)

    response = requests.post(url,
                             data=payload,
                             headers={
                                 "Content-Type": "multipart/related; boundary=xxoo1707a7a80f1xxoo",
                                 'Authorization': 'Bearer '+auth.token()
                             }
                             )
    if configure.debug:
        print(url)
        print(payload)
        print(response.content)
    if response.status_code != 201:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))
