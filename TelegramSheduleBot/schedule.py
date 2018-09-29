import requests
import config
import datetime
import re


def getIdGroup(name):
    req = requests.get(config.main_url + config.list_group)
    data = req.json()
    print(data)
    for i in data['data']:
        if re.search(name, i['name']):
            return i['id']


def get_schedule_group_current_day(id):
    url = config.main_url + config.shedule_group + str(id)
    req = requests.get(url)
    data_json = req.json()
    date = datetime.date.today()
    schedule_current_day = data_json['data'][str(date)]
    # sheduleCurrentDay = data_json.get['data'].get(str(date))
    print(schedule_current_day)
    return schedule_current_day


def get_schedule_group(id):
    url = config.main_url + config.shedule_group + str(id)
    req = requests.get(url)
    data_json = req.json()
    return data_json['data']


def get_current_date():
    return str(datetime.date.today())
