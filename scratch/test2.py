# Import Raspberry Pi GPIO library
import datetime

import RPi.GPIO as GPIO


# Map to gpio, follows board format (1 - ...)
# Run 'pinout' on shell in rpi to get mappings.
pin_out = {
    'email': 3,     # GPIO2
    'call': 13,     # GPIO27
    'meeting': 7,   # GPIO2
    'admin': 5,     # GPIO3
    'stop': 11,     # GPIO17
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


def start_call(channel):
    print("Call button was pushed.")


def start_meeting(channel):
    print("Meeting button was pushed.")


# Stop tracking and save to timecamp
def stop_tracking(channel):
    # Only track if it's currently running. Otherwise ignore it.
    print("Stop button pressed")

    if global_state['running'] is True:
        global_state['end_time'] = get_current_time()
        global_state['running'] = False
        print("> stopping task and recording")
        print(global_state)


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
GPIO.add_event_detect(pin_out['email'], GPIO.RISING, callback=start_email)
GPIO.add_event_detect(pin_out['call'], GPIO.RISING, callback=start_call)
GPIO.add_event_detect(pin_out['meeting'], GPIO.RISING, callback=start_meeting)
GPIO.add_event_detect(pin_out['admin'], GPIO.RISING, callback=start_admin)
GPIO.add_event_detect(pin_out['stop'], GPIO.RISING, callback=stop_tracking)

message = input("Press enter to quit\n\n") # Run until someone presses enter

# Clean up
GPIO.cleanup()

