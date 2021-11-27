import RPi.GPIO as GPIO
from log import tlog


def tracking_led_on():
    tlog("LED on")
    GPIO.output(23, GPIO.HIGH)


def tracking_led_off():
    tlog("LED off")
    GPIO.output(23, GPIO.LOW)
