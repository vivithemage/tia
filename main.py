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

tc_endpoints = {
    'entries': 'https://app.timecamp.com/third_party/api/entries'
}


# TM
# 'authorization': "9cea44b6316b521a673556d2a4",
# RS
# 'authorization': "90c3737f69122ea9ea321928e6",
api_key = '90c3737f69122ea9ea321928e6'


# returns current time in timecamp format.
class Tracking:
    def _record(start, end, description):
        today = date.today()

        payload = {'date': today.strftime("%Y-%m-%d"),
                   'start': start,
                   'end': end,
                   'note': description,
                   'description': description
                   }

        headers = {
            'authorization': api_key,
            'Content-Type': "application/json"
        }

        response = requests.request("POST", tc_endpoints['entries'], 
                                    data=json.dumps(payload), 
                                    headers=headers)

        print("> timecamp response")
        print(response.text)


    def _get_current_time(self):
        today = datetime.datetime.now()
        time_string = today.strftime("%H:%M:%S")
        print(time_string)

        return time_string


    def stop(self):
        print("Stop request (either button or start)")

        if global_state['running'] is True:
            print("stopping " + task_name)
            global_state['end_time'] = get_current_time()
            global_state['running'] = False
            print("> stopping task and recording")
            self._record(start=global_state['start_time'], end=global_state['end_time'], description=global_state['current_task'])
            print(global_state)


    def start(self, task_name):
        print(task_name + "button was pushed.")
       
        # Stop task before starting a new one (just a precaution)
        self.stop()
        
        if global_state['running'] is not True:
            print("starting to track " + task_name)
            global_state['running'] = True
            global_state['current_task'] = task_name 
            global_state['start_time'] = self._get_current_time()


# Start Triggers
def start_email(channel):
    t = Tracking()
    t.start('email') 

def start_admin(channel):
    t = Tracking()
    t.start('admin') 

def start_call(channel):
    t = Tracking()
    t.start('call') 

def start_meeting(channel):
    t = Tracking()
    t.start('meeting') 

# Stop tracking and save to timecamp
def stop_tracking(channel):
    t = Tracking()
    t.stop()


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

