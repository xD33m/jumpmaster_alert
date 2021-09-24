from dotenv import load_dotenv
import sys
import win32api
import win32con
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def loadEnv():
    load_dotenv(dotenv_path=resource_path(".env"))


def getEnvId():
    userId = os.getlogin()
    if userId == "juliu":
        return "JULIUS_ID"
    elif userId == "lucas":
        return "LUCAS_ID"
    elif userId == "felix":
        return "FELIX_ID"


def is1080pMonitor():
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    is1080p = True if 1070 <= height <= 1090 else False
    return is1080p


def getNeedleImgPath(isJumpmaster):
    is1080p = is1080pMonitor()

    jumpmasterImgPath1440 = resource_path('./images/jumpIcon1440.png')
    jumpmasterImgPath1080 = resource_path('./images/jumpIcon1080.png')

    charImgPath1440 = resource_path('./images/bloodIcon1440.png')
    charImgPath1080 = resource_path('./images/bloodIcon1080.png')

    if isJumpmaster and is1080p:
        return jumpmasterImgPath1080
    elif isJumpmaster and not is1080p:
        return jumpmasterImgPath1440
    elif not isJumpmaster and is1080p:
        return charImgPath1080
    else:
        return charImgPath1440


def getNeedlePostion(isJumpmaster):
    is1080p = is1080pMonitor()

    jumpmasterIconPos1440 = {'left': 1100, 'top': 1076, 'width': 80,
                             'height': 80}
    jumpmasterIconPos1080 = {'left': 835, 'top': 817, 'width': 70,
                             'height': 70}
    charIconPos1440 = {'left': 1509, 'top': 435, 'width': 70,
                       'height': 70}
    charIconPos1080 = {'left': 1123, 'top': 328, 'width': 70,
                       'height': 70}

    if isJumpmaster and is1080p:
        return jumpmasterIconPos1080
    elif isJumpmaster and not is1080p:
        return jumpmasterIconPos1440
    elif not isJumpmaster and is1080p:
        return charIconPos1080
    else:
        return charIconPos1440
