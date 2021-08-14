import json
import requests

from datetime import date
import datetime

import RPi.GPIO as GPIO


global_state = {
    'running': False,
    'current_task': 'unknown',
    'start_time': None,
    'end_time': None
}

tc_endpoints = {
    'entries': 'https://app.timecamp.com/third_party/api/entries'
}

# Seperate api keys, makes it easy to switch during testing
api_key = {
    'rs':  '90c3737f69122ea9ea321928e6', # My work timecamp
    'rst': '',                           # test timecamp
    'tm':  '9cea44b6316b521a673556d2a4'  # Tom's timecamp
}


class Tasks:
    def pull(self):
        print("pulling all tasks")
        api = Timecamp_Api()
        tasks = api.get_tasks()
    
    def populate(self):
        print("populating tasks")

    def get_id(self, name):
        print("getting id based on name")


class Buttons:
    def setup(self):
        # Ignore warning for now
        GPIO.setwarnings(False)

        # Use physical pin numbering
        GPIO.setmode(GPIO.BOARD)
        
        # Map to gpio, follows board format (1 - ...)
        # Run 'pinout' on shell in rpi to get mappings.
        pin_out = {
            'email': 3,    
            'call': 13,    
            'meeting': 11,
            'admin': 5,  
            'stop': 7,  
        }

        # Set pins for each button
        for pin in pin_out:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup event for each button on rising pin
        GPIO.add_event_detect(pin_out['email'], GPIO.RISING, callback=start_email, bouncetime=200)
        GPIO.add_event_detect(pin_out['call'], GPIO.RISING, callback=start_call, bouncetime=200)
        GPIO.add_event_detect(pin_out['meeting'], GPIO.RISING, callback=start_meeting, bouncetime=200)
        GPIO.add_event_detect(pin_out['admin'], GPIO.RISING, callback=start_admin, bouncetime=200)
        GPIO.add_event_detect(pin_out['stop'], GPIO.RISING, callback=stop_tracking, bouncetime=200)

        # Clean up
        GPIO.cleanup()


# TODO: Initialize led's for notififications
class Indicators:
    def setup(self):
        print("Led setup")

    def running(self):
        print("Led 2 (red) on indicating task running")
    
    def not_running(self):
        print("Led 2 (red) off indicating no task is active")

    def ready(self):
        print("Led 1 (green) on indicating ready for input")

    def booting(self):
        print("Led 1 (green) is off")


# All interactions with translations.
class Translation_Api:
    def send_file(self, filename):
        print("sending file to translator")

    def _get_status(self):
        print("Getting status")

    def get_text(self):
        print("sending file to translator")


# All interactions with timecamp.
class Timecamp_Api:
    def record_entry(self, start, end, description):
        today = date.today()

        payload = {'date': today.strftime("%Y-%m-%d"),
                   'start': start,
                   'end': end,
                   'note': description,
                   'description': description
                   }

        headers = {
            'authorization': api_key['rst'],
            'Content-Type': "application/json"
        }

        response = requests.request("POST", tc_endpoints['entries'], 
                                    data=json.dumps(payload), 
                                    headers=headers)

        print("> timecamp response")
        print(response.text)


    def start_timer(self):
        print("starting timer")


    def stop_timer(self):
        print("stop timer")

    def get_tasks(self):
        print("getting tasks")


class Tracking:

    def _task_running(self):
        if global_state['running'] is True:

    
    def _get_current_time(self):
        today = datetime.datetime.now()
        time_string = today.strftime("%H:%M:%S")
        print(time_string)

        return time_string


    def stop(self):
        print("Stop request (either button or start)")

        if self._task_running():
            print("stopping " + task_name)
            global_state['end_time'] = get_current_time()
            global_state['running'] = False
            
            print("> stopping task and recording")
            api = Timecamp_Api()
            api.record_entry(start=global_state['start_time'], 
                              end=global_state['end_time'], 
                              description=global_state['current_task'])
            
            print(global_state)


    def start(self, task_name):
        print(task_name + "button was pushed.")
       
        # Stop task before starting a new one 
        # This is just a precaution in case one is already running.
        self.stop()
        
        if self._task_running() is not True:
            print("starting to track " + task_name)
            global_state['running'] = True
            global_state['current_task'] = task_name 
            global_state['start_time'] = self._get_current_time()


# Start Triggers TODO - change this to a single function by padding argument 
# in event trigger
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

    print("Initializing buttons...")
    buttons = Buttons()
    buttons.setup()

    print("Initializing notification LED's...")
    led = Indicators()
    led.setup()

    print("Populating tasks...")
    tasks = Tasks()
    tasks.populate()

    led.ready()
    print("Ready!")
    message = input("Press enter to quit\n\n")  # Run until someone presses enter



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tia()

