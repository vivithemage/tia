# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO


# Map to gpio, follows board format (1 - ...)
# Run 'pinout' on shell in rpi to get mappings.
pin_out = {
    'email': 3,     # GPIO2
    'call': 5,      # GPIO3
    'meeting': 7,   # GPIO2
    'admin': 11,    # GPIO17
    'stop': 13,     # GPIO27
}


# Start Triggers
def start_email(channel):
    print("Email button was pushed!")


def start_admin(channel):
    print("Admin button was pushed!")


def start_call(channel):
    print("Call button was pushed!")


def start_meeting(channel):
    print("Meeting button was pushed!")


# Stop tracking and save to timecamp
def stop_tracking(channel):
    print("Button was pushed!")


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
