import json
import os
import configparser
import requests

home = os.path.expanduser('~')

debug = False
device = None


def fetch_endpoint():
    response = requests.get("https://config.mycloud.com/config/v1/config")

    if response.status_code != 200:
        raise Exception("Endpoint Error !!! [{}][{}]".format(
            response.status_code, response.content))

    config = json.loads(response.content)['data']
    # print(config)
    write('cloud.service.urls', config['componentMap']['cloud.service.urls'])


def get(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))
    return config[section][key]

# def save(section, key, value):
#     config = configparser.ConfigParser()
#     config.read(os.path.join(home, 'mycloudhome.ini'))
#     config['section'][key] = value

#     with open(os.path.join(home, 'mycloudhome.ini'), 'w') as configfile:
#         config.write(configfile)


def save_token(token):
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))
    config['auth'] = token

    with open(os.path.join(home, 'mycloudhome.ini'), 'w') as configfile:
        config.write(configfile)


def get_token():
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))
    return config['auth']['id_token']


def save_profiles(devices, user):
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))

    for device in devices:
        profile_name = device['deviceId']
        config[profile_name] = device['network']
        config[profile_name]['deviceId'] = device['deviceId']
        config[profile_name]['serialNumber'] = device['serialNumber']
        config[profile_name]['name'] = device['name']
        config[profile_name]['email'] = user['email']
        config[profile_name]['name'] = user['name']
        config[profile_name]['user_id'] = user['user_id']
        config[profile_name]['first_name'] = user['user_metadata']['first_name']
        config[profile_name]['last_name'] = user['user_metadata']['last_name']
        config[profile_name]['lang'] = user['user_metadata']['lang']
        config[profile_name]['time_zone_name'] = user['user_metadata']['time_zone_name']

    with open(os.path.join(home, 'mycloudhome.ini'), 'w') as configfile:
        config.write(configfile)


def get_default_profile():
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))
    sections = config.sections()
    sections.remove('cloud.service.urls')
    sections.remove('auth')

    if device is not None and device in sections:
        return device

    if os.getenv('WD_DEVICE') and os.getenv('WD_DEVICE') in sections:
        return os.getenv('WD_DEVICE')

    return sections[0]


def write(section, configuration):
    config = configparser.ConfigParser()
    config.read(os.path.join(home, 'mycloudhome.ini'))
    config[section] = configuration

    with open(os.path.join(home, 'mycloudhome.ini'), 'w') as configfile:
        config.write(configfile)
