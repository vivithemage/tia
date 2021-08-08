import json
import requests
from datetime import date


def record(start, end, description):
    today = date.today()
    url = "https://app.timecamp.com/third_party/api/entries"

    payload = {'date': today.strftime("%Y-%m-%d"),
               'start': start,
               'end': end,
               'note': 'email note',
               'description': description
               }

    headers = {
        'authorization': "cd9eab8a7b4551e664c2e0a9ed",
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print(response.text)


def tia():
    print("starting tia...")
    record(start='19:05:47', end='20:21:31', description='email description')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
