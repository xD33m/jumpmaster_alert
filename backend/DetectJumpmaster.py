import win32gui
import win32ui
import win32con
import win32api
import json
import requests
import time
import numpy
import cv2
import sys
import os
from playsound import playsound
from random import randrange
from dotenv import load_dotenv


currentIteration = 1


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


def sendDiscordDM(message):
    userAuthToken = os.getenv('DISCORD_BOT_TOKEN')
    print(userAuthToken)

    dmEndpoint = "https://discordapp.com/api/users/@me/channels"
    dmHeaders = {"Authorization": f"Bot {userAuthToken}",
                 "Content-Type": "application/json",
                 "User-Agent": "Chrome/94.0.4606.31 ",
                 "Accept-Language": "en-GB"}

    envID = getEnvId()
    recipientID = os.getenv(envID)
    recipientJSON = json.dumps({"recipient_id": recipientID})
    response = requests.post(dmEndpoint, headers=dmHeaders, data=recipientJSON)
    response_dict = json.loads(response.text)
    userID = response_dict['id']

    msgURL = f"https://discordapp.com/api/channels/{userID}/messages"
    msgHeaders = {"Authorization": f"Bot {userAuthToken}",
                  "Content-Type": "application/json", }

    msgJSON = json.dumps({"content": message})
    requests.post(msgURL, headers=msgHeaders, data=msgJSON)


def lookForApex(sc, hwnd):
    event = sc.enter(1, 1, lookForApex, (sc, hwnd,))
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd != 0:
        print('Apex detected!')
        sc.cancel(event)
        detect_champion_selection(sc)


def takeScreenshot(sc, isJumpmaster, event):
    # https://answers.opencv.org/question/229026/help-with-optimization-opencv-python/

    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd == 0:
        print("Apex not found. Waiting for Apex to start...")
        lookForApex(sc, hwnd)
        sc.cancel(event)
        return None, None

    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

    is1080p = True if 1070 <= height <= 1090 else False

    filePath, imgPosition = getIconAndPosition(isJumpmaster, is1080p)

    imgLeft = imgPosition['left']
    imgTop = imgPosition['top']
    imgWidth = imgPosition['width']
    imgHeight = imgPosition['height']

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()

    saveBitMap.CreateCompatibleBitmap(mfcDC, imgWidth, imgHeight)
    saveDC.SelectObject(saveBitMap)

    saveDC.BitBlt((0, 0), (imgWidth, imgHeight), mfcDC,
                  (imgLeft, imgTop), win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = numpy.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (imgHeight, imgWidth, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    img_gray = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2GRAY)
    return img_gray, filePath


def image_comp(sc, isJumpmaster, event):
    img_gray, filePath = takeScreenshot(sc, isJumpmaster, event)
    if img_gray is None or filePath is None:
        return None
    imgToCompare = cv2.imread(filePath, 0)

    res = cv2.matchTemplate(img_gray, imgToCompare, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # cv2.imshow("Image", img_gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('Fenster wird geschlossen')
    return max_val


def getIconAndPosition(isJumpmaster, is1080p):
    jumpmasterFilePath1440 = resource_path('./images/jumpIcon1440.png')
    jumpmasterFilePath1080 = resource_path('./images/jumpIcon1080.png')
    jumpmasterIconPosition1440 = {'left': 1100, 'top': 1076,
                                  'width': 80, 'height': 80}
    jumpmasterIconPosition1080 = {'left': 835, 'top': 817,
                                  'width': 70, 'height': 70}

    charFilePath1440 = resource_path('./images/bloodIcon1440.png')
    charFilePath1080 = resource_path('./images/bloodIcon1080.png')
    charIconPosition1440 = {'left': 1509, 'top': 435,
                            'width': 70, 'height': 70}
    charIconPosition1080 = {'left': 1123, 'top': 328,
                            'width': 70, 'height': 70}

    if isJumpmaster and is1080p:
        return jumpmasterFilePath1080, jumpmasterIconPosition1080
    elif isJumpmaster and not is1080p:
        return jumpmasterFilePath1440, jumpmasterIconPosition1440
    elif not isJumpmaster and is1080p:
        return charFilePath1080, charIconPosition1080
    else:
        return charFilePath1440, charIconPosition1440


def playRandomSound():
    randomIndex = randrange(8)  # 0-7
    soundToPlay = resource_path(f'sounds\\voice{randomIndex+1}.wav')
    playsound(soundToPlay)


def detect_jumpmaster(sc,):
    global currentIteration
    maxIteration = 120

    event = sc.enter(1, 1, detect_jumpmaster, (sc,))

    max_val = image_comp(sc, True, event)

    print(
        f"Jumpmaster detected: {'true  ' if max_val >= 0.8 else 'false'} - {currentIteration}/{maxIteration}", end='\r', flush=True)

    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        playRandomSound()
        sendDiscordDM("DU BIST JUMPASTER")
        sc.cancel(event)
        print()  # new line
        detect_champion_selection(sc)
        currentIteration = 0
    elif(currentIteration == maxIteration):
        sc.cancel(event)
        print()  # new line
        detect_champion_selection(sc)
        currentIteration = 0


def detect_champion_selection(sc):
    event = sc.enter(20, 1, detect_champion_selection, (sc,))
    max_val = image_comp(sc, False, event)
    if max_val is None:
        return

    print(
        f"Champion selection detected: {'true  ' if max_val >= 0.8 else 'false'}")

    if max_val >= 0.8:
        sc.cancel(event)
        print()  # new line
        detect_jumpmaster(sc)
