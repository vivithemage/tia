import RPi.GPIO as gpio
from recorder import Recorder


# def rising(channel):
#     global recfile
#     gpio.remove_event_detect(3)
#     print ('Button up')
#     gpio.add_event_detect(3, gpio.FALLING, callback=falling, bouncetime=10)
#     recfile.stop_recording()
#     recfile.close()
#
#
# def falling(channel):
#     global recfile
#     gpio.remove_event_detect(3)
#     print ('Button down')
#     gpio.add_event_detect(3, gpio.RISING, callback=rising, bouncetime=10)
#     rec = Recorder(channels=2)
#     recfile = rec.open('nonblocking.wav', 'wb')
#     recfile.start_recording()

def rising(channel):
    print("released")
    gpio.remove_event_detect(3)
    gpio.add_event_detect(3, gpio.FALLING, callback=falling, bouncetime=10)


def falling(channel):
    print("pressed")
    gpio.remove_event_detect(3)
    gpio.add_event_detect(3, gpio.RISING, callback=rising, bouncetime=10)


def tia():
    print("starting tia...")

    # Ignore warning for now
    gpio.setwarnings(False)

    gpio.setmode(gpio.BOARD)
    gpio.setup(3, gpio.IN, pull_up_down=gpio.PUD_UP)

    gpio.add_event_detect(3, gpio.FALLING, callback=falling, bouncetime=10)

    message = input("Press enter to quit\n\n")  # Run until someone presses enter

    gpio.cleanup()


if __name__ == '__main__':
    tia()

