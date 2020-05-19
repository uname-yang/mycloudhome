import json
import os

import requests

import mycloudhome.configure as configure
import mycloudhome.auth as auth
import mycloudhome.utils as utils


def upload(localPath, wdUri):
    dir_id = utils.convert_wd_path_to_wd_id(wdUri)
    file_name = utils.get_local_file_name(localPath)

    localtion = create_resumable_file(file_name, dir_id)

    url = configure.get(configure.get_default_profile(),
                        'externaluri') + localtion + '/resumable/content'

    response = requests.put(url, data=open(localPath, 'rb'), headers={
                            'Authorization': 'Bearer '+auth.token(), 'Content-Type': 'application/octet-stream'})

    if configure.debug:
        print("URL: {}".format(url))
        print(response)

    mark_resumable_file_as_done(localtion)


def create_resumable_file(name, parentID):
    url = configure.get(configure.get_default_profile(),
                        'externaluri') + '/sdk/v2/files/resumable?resolveNameConflict=1&done=false'

    payload = """
--foo

{{"name":"{}","parentID":"{}"}}
--foo

--foo--
""".format(name, parentID)

    response = requests.post(url,
                             data=payload,
                             headers={
                                 "Content-Type": "multipart/related; boundary=foo",
                                 'Authorization': 'Bearer '+auth.token()
                             }
                             )
    if configure.debug:
        print("URL: {}".format(url))
        print("Payload: {}".format(payload))
        print(response)  # 201
        print("Header: {}".format(response.headers))
    if response.status_code != 201:
        raise Exception("FILE MANAGEMENT Error !!! [{}][{}]".format(
            response.status_code, response.content))

    return response.headers['Location']


def mark_resumable_file_as_done(fileLocation):
    url = configure.get(configure.get_default_profile(),
                        'externaluri') + fileLocation + '/resumable/content?done=true'

    response = requests.put(
        url, headers={'Authorization': 'Bearer '+auth.token()})

    if configure.debug:
        print("URL: {}".format(url))
        print(response)  # 204
