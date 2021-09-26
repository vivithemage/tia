import RPi.GPIO as GPIO


buttonPin = 3


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # initialize button pin


def loop():
    while True:
        while GPIO.input(buttonPin) == GPIO.LOW:  # if button is pressed
            print("held")

        if GPIO.input(buttonPin) == GPIO.HIGH:
            print("released")


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When Ctrl + C is pressed, execute this
        destroy()