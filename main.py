import os
import sys
import threading
from time import sleep

import config
import logger

logger.Logger.init()

import traceback
import keyboard
import basics

isWork = False


def stopMainLoop(func=None):
    if func is not None:
        func()
    global isWork
    isWork = False


def startMainLoop():
    global isWork
    isWork = True

    basics.MAP = basics.Map(basics.configs["MAP"])

    logger.Logger.log(basics.MAP.ObjList.getObjs())
    mainThread = threading.Thread(target=MainLoop)
    uiThread = threading.Thread(target=DrawLoop)
    fixedThread = threading.Thread(target=FixedLoop)

    mainThread.start()
    fixedThread.start()
    uiThread.start()


def OnClose(event):
    global isWork
    logger.Logger.stop('Stopped by closing window or fatal error')
    isWork = False

    '''if event in [win32con.CTRL_C_EVENT,
                 win32con.CTRL_LOGOFF_EVENT,
                 win32con.CTRL_BREAK_EVENT,
                 win32con.CTRL_SHUTDOWN_EVENT,d
                 win32con.CTRL_CLOSE_EVENT,
                 signal.CTRL_C_EVENT,
                 signal.CTRL_BREAK_EVENT] and isWork:...'''


if os.name == "nt":
    try:
        import win32api

        win32api.SetConsoleCtrlHandler(OnClose, True)
    except ImportError:
        version = '.'.join(map(str, sys.version_info[:2]))
        raise Exception('pywin32 not installed for Python  ' + version)
else:
    import signal

    signal.signal(signal.SIGTERM, OnClose)


def DrawLoop():
    bef = ''
    while isWork:
        i = str(basics.MAP.matrix) + str(basics.MAP.ui)
        if bef != i and not basics.MAP.matrix.isEmpty:
            basics.MAP.ui.cls()
            bef = i
            print(i)
            # basics.UI.printStrAtPos('', 50, 0)
            basics.MAP.matrix = basics.DrawMatrix()
        else:
            sleep(1 / 100)


def FixedLoop():
    try:
        while isWork:
            sleep(config.configs.get("FIXED REPETITIONS", 0.02))
            for i in basics.MAP.ObjList.getObjs():
                if i.enabled:
                    i.fixed_upd()
    except (Exception, BaseException) as e:
        stopMainLoop()
        print("\n[Exception cached in Fixed Update]")
        logger.Logger.log(f'{str(e)}\n' + '\n'.join(traceback.format_tb(e.__traceback__)), logger.Logger.FixedError)


def MainLoop():
    try:
        for y in basics.MAP.ObjList.getObjs():
            y.transform.upd()
        for y in basics.MAP.ObjList.getObjs():
            y.awake()
        for y in basics.MAP.ObjList.getObjs():
            y.start()

        while isWork:
            sleep(1 / config.configs.get('FPS', 15))
            if keyboard.is_pressed('shift+esc'):
                stopMainLoop()
                continue
            for i in basics.MAP.ObjList.getObjs():
                if i.enabled:
                    i.upd()
            for i in basics.MAP.ObjList.getObjs():
                if i.enabled:
                    i.late_upd()
        stopMainLoop()
    except (Exception, BaseException) as e:
        stopMainLoop()
        print("\n[Exception cached]")
        logger.Logger.log(f'{str(e)}\n' + '\n'.join(traceback.format_tb(e.__traceback__)), logger.Logger.Error)
    print("\n[Program is over]")
    logger.Logger.stop()
    input()


if __name__ == '__main__':
    startMainLoop()
