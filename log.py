from datetime import datetime


def tlog(message):
    print('tia - ' + str(datetime.now()) + ' >> ' + message)