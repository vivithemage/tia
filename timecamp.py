import json
import requests
import xmltodict

from log import tlog
from datetime import date


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
        # tlog("timecamp response")
        #tlog(data_dict)

    def start_timer(self, task_id):
        tlog("Starting timer")
        payload = {'action': 'start',
                   'task_id': task_id}

        # TODO: issue lies with this triggering the whole process again.
        response = requests.request("POST", tc_endpoints['timer'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        tlog("Timecamp timer start response")
        data_dict = xmltodict.parse(response.text)

        return data_dict.get('xml')['entry_id']

    def set_description(self, entry_id, description):
        tlog("Starting timer")
        payload = {'id': entry_id, 'description': description}

        # TODO: issue lies with this triggering the whole process again.
        response = requests.request("PUT", tc_endpoints['entries'],
                                    data=json.dumps(payload),
                                    headers=self.headers)

        data_dict = xmltodict.parse(response.text)
        print(data_dict)

    def stop_timer(self):
        tlog("stop timer")

    def get_tasks(self):
        tlog("getting tasks")
