import datetime
import os
from typing import Type


class Logger:
    class LogMessage:
        ...

    class Init(LogMessage):
        ...

    class Stop(LogMessage):
        ...

    class Error(LogMessage):
        ...

    class FixedError(Error):
        ...

    class LoggerError(Error):
        ...

    class DrawCall(LogMessage):
        ...

    @staticmethod
    def log(message: object = None, messageType: Type[LogMessage] = LogMessage):
        s = str(message)
        # print(f'[{datetime.datetime.now()}]: ' + s)
        with open(f'logs\\_now.log', 'ab') as f:
            f.write(bytes(
                f'[{messageType.__name__.upper()}][{datetime.datetime.now()}]{": " if message is not None and message != "" else ""}{s if message is not None else ""}\n',
                'utf-8'))

    @staticmethod
    def init():
        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '\\logs'):
            os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '\\logs')
        if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '\\logs\\_now.log'):
            Logger.log("_now.log was not deleted", Logger.LoggerError)
            Logger.stop()
        Logger.log(None, Logger.Init)

    @staticmethod
    def stop(s='Program is over'):
        Logger.log(s, Logger.Stop)
        orr = ''
        with open(f'logs\\_now.log', 'rb') as orig:
            orr = orig.read()
        with open(f'logs\\log_{datetime.datetime.now()}.log'.replace(':', '-'), 'wb') as neww:
            neww.write(orr)
        os.remove(f'logs\\_now.log')
