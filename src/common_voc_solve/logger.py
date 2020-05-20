import datetime


def log(message):
    now = datetime.datetime.now()
    print("{0} - {1}".format(now.strftime("%Y-%m-%d %H:%M:%S"), message))
    return
