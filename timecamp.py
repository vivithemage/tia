import json
import time

import requests
from log import tlog
from datetime import date
import xmltodict

tc_endpoints = {
    'entries': 'https://app.timecamp.com/third_party/api/entries',
    'timer': 'https://app.timecamp.com/third_party/api/timer'
}

# Seperate api keys, makes it easy to switch during testing
api_key = {
    'rs':  '90c3737f69122ea9ea321928e6', # My work timecamp
    'rst': 'cd9eab8a7b4551e664c2e0a9ed', # test timecamp
    'tm':  '9cea44b6316b521a673556d2a4'  # Tom's timecamp
}


# All interactions with timecamp.
class TimecampApi:
    def __init__(self):
        self.headers = {
            'authorization': api_key['rst'],
            'Content-Type': "application/json"
        }

    def record_entry(self, start, end, description):
        today = date.today()

        payload = {'date': today.strftime("%Y-%m-%d"),
                   'start': start,
                   'end': end,
                   'note': description,
                   'description': description
                   }

        response = requests.request("POST", tc_endpoints['entries'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        #data_dict = xmltodict.parse(response.text)
        tlog("> timecamp response")
        #tlog(data_dict)

    def start_timer(self):
        tlog("starting timer")
        payload = {'action': 'start'}

        # time.sleep(2)
        # TODO: issue lies with this triggering the whole process again.
        response = requests.request("POST", tc_endpoints['timer'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        tlog("> timecamp timer start response")
        data_dict = xmltodict.parse(response.text)

        tlog(data_dict.items())

    def stop_timer(self):
        tlog("stop timer")

    def get_tasks(self):
        tlog("getting tasks")
