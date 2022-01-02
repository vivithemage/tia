import RPi.GPIO as gpio


def falling(channel):
    print("pressed")


def tia():
    print("Press button test...")

    button_pin = 5

    # Ignore warning for now
    gpio.setwarnings(False)

    gpio.setmode(gpio.BOARD)
    gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    gpio.add_event_detect(button_pin, gpio.FALLING, callback=falling, bouncetime=10)

    message = input("Press enter to quit\n\n")  # Run until someone presses enter

    gpio.cleanup()


if __name__ == '__main__':
    tia()

