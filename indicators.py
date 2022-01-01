import RPi.GPIO as GPIO
from log import tlog


def tracking_led_on():
    tlog("Tracking LED on")
    GPIO.output(23, GPIO.HIGH)


def tracking_led_off():
    tlog("Tracking LED off")
    GPIO.output(23, GPIO.LOW)
