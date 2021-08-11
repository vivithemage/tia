import json
import requests

from datetime import date
import datetime

import RPi.GPIO as GPIO

# Map to gpio, follows board format (1 - ...)
# Run 'pinout' on shell in rpi to get mappings.
pin_out = {
    'email': 3,     # GPIO2
    'call': 13,     # GPIO27
    'meeting': 11,   # GPIO2
    'admin': 5,     # GPIO3
    'stop': 7,     # GPIO17
}

global_state = {
    'running': False,
    'current_task': 'unknown',
    'start_time': None,
    'end_time': None
}


# returns current time in timecamp format.
def get_current_time():
    today = datetime.datetime.now()
    time_string = today.strftime("%H:%M:%S")
    print(time_string)

    return time_string


# Start Triggers
def start_email(channel):
    print("Email button was pushed.")

    if global_state['running'] is not True:
        print("> Tracking email task!")
        global_state['running'] = True
        global_state['current_task'] = 'email'
        global_state['start_time'] = get_current_time()


def start_admin(channel):
    print("Admin button was pushed.")

    if global_state['running'] is not True:
        print("> Tracking admin task!")
        global_state['running'] = True
        global_state['current_task'] = 'admin'
        global_state['start_time'] = get_current_time()


def start_call(channel):
    print("Call button was pushed.")

    if global_state['running'] is not True:
        print("> Tracking call task!")
        global_state['running'] = True
        global_state['current_task'] = 'call'
        global_state['start_time'] = get_current_time()


def start_meeting(channel):
    print("Meeting button was pushed.")

    if global_state['running'] is not True:
        print("> Tracking meeting task!")
        global_state['running'] = True
        global_state['current_task'] = 'meeting'
        global_state['start_time'] = get_current_time()


# Stop tracking and save to timecamp
def stop_tracking(channel):
    # Only track if it's currently running. Otherwise ignore it.
    print("Stop button pressed")

    if global_state['running'] is True:
        global_state['end_time'] = get_current_time()
        global_state['running'] = False
        print("> stopping task and recording")
        record(start=global_state['start_time'], end=global_state['end_time'], description=global_state['current_task'])
        print(global_state)


def record(start, end, description):
    today = date.today()
    url = "https://app.timecamp.com/third_party/api/entries"

    payload = {'date': today.strftime("%Y-%m-%d"),
               'start': start,
               'end': end,
               'note': description,
               'description': description
               }

    # TM
    # 'authorization': "9cea44b6316b521a673556d2a4",
    # RS
    # 'authorization': "90c3737f69122ea9ea321928e6",
    headers = {
    	'authorization': "90c3737f69122ea9ea321928e6",
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print("> timecamp response")
    print(response.text)


def tia():
    print("starting tia...")
    # Ignore warning for now
    GPIO.setwarnings(False)

    # Use physical pin numbering
    GPIO.setmode(GPIO.BOARD)

    # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(pin_out['email'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_out['call'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_out['meeting'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_out['admin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_out['stop'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup event for each button on rising pin
    GPIO.add_event_detect(pin_out['email'], GPIO.RISING, callback=start_email, bouncetime=200)
    GPIO.add_event_detect(pin_out['call'], GPIO.RISING, callback=start_call, bouncetime=200)
    GPIO.add_event_detect(pin_out['meeting'], GPIO.RISING, callback=start_meeting, bouncetime=200)
    GPIO.add_event_detect(pin_out['admin'], GPIO.RISING, callback=start_admin, bouncetime=200)
    GPIO.add_event_detect(pin_out['stop'], GPIO.RISING, callback=stop_tracking, bouncetime=200)

    message = input("Press enter to quit\n\n")  # Run until someone presses enter

    # Clean up
    GPIO.cleanup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
