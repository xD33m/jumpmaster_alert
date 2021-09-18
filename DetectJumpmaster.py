import json
import requests
import time
import sched
import mss
import numpy
import cv2
import os
from playsound import playsound
from random import randrange
from dotenv import load_dotenv
load_dotenv()


print("Jumpmaster detection started")

# https://stackoverflow.com/a/474543
s = sched.scheduler(time.time, time.sleep)
currentIteration = 0


# braucht man für die exe: https://stackoverflow.com/a/13790741
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def getEnvId():
    userId = os.getlogin()
    if userId == "juliu":
        return "JULIUS_ID"
    elif userId == "lucas":
        return "LUCAS_ID"
    else:
        return "TIM_ID"


def sendDiscordDM(message):
    userAuthToken = os.getenv('DISCORD_BOT_TOKEN')

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


def image_comp(isJumpmaster):
    sct = mss.mss()

    monitorHeight = sct.monitors[0]['height']
    is1080p = True if 1070<= monitorHeight<= 1090 else False # bei mir ist's 1081 bei 1080p?

    filePath, iconPosition = getIconAndPosition(isJumpmaster, is1080p)
    imgToCompare = cv2.imread(filePath, 0)

    img = numpy.asarray(sct.grab(iconPosition))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, imgToCompare, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # cv2.imshow("Image", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('Fenster wird geschlossen')
    return max_val

def getIconAndPosition(isJumpmaster, is1080p):
    jumpmasterFilePath1440 = resource_path('./images/jumpIcon1440.png')
    jumpmasterFilePath1080 = resource_path('./images/jumpIcon1080.png')
    jumpmasterIconPosition1440 = {'left': 1100, 'top': 1076, 'width': 80, 'height': 80}
    jumpmasterIconPosition1080 = {'left': 835, 'top': 817, 'width': 70, 'height': 70}

    charFilePath1440 = resource_path('./images/bloodIcon1440.png')
    charFilePath1080 = resource_path('./images/bloodIcon1080.png')
    charIconPosition1440 = {'left': 1509, 'top': 435, 'width': 70, 'height': 70}
    charIconPosition1080 = {'left': 1123, 'top': 328, 'width': 70, 'height': 70}
    if isJumpmaster and is1080p:
        return  jumpmasterFilePath1080, jumpmasterIconPosition1080
    elif isJumpmaster and not is1080p:
        return jumpmasterFilePath1440, jumpmasterIconPosition1440
    elif not isJumpmaster and is1080p:
        print('here')
        return charFilePath1080, charIconPosition1080
    else:
        return charFilePath1440, charIconPosition1440

def playRandomSound():
    randomIndex = randrange(8)  # 0-7
    soundToPlay = resource_path(f'sounds/voice{randomIndex+1}.mp3')
    playsound(soundToPlay)

def detect_jumpmaster(sc):
    global currentIteration
    maxIteration = 120
    
    max_val = image_comp(isJumpmaster=True)

    print(
        f"jumpmaster detected: {'true' if max_val >= 0.8 else 'false'} - {currentIteration}/{maxIteration}")

    event = s.enter(1, 1, detect_jumpmaster, (sc,))
    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        sendDiscordDM("DU BIST JUMPASTER DU NOOB")
        playRandomSound()
        s.cancel(event)
        detect_champion_selection(sc)
        currentIteration = 0
    elif(currentIteration == maxIteration):
        s.cancel(event)
        detect_champion_selection(sc)
        currentIteration = 0


def detect_champion_selection(sc):
    max_val = image_comp(isJumpmaster=False)
    print(
        f"character selection detected: {'true' if max_val >= 0.8 else 'false'}")

    event = s.enter(20, 1, detect_champion_selection, (sc,))
    if max_val >= 0.8:
        s.cancel(event)
        detect_jumpmaster(sc)


s.enter(1, 1, detect_champion_selection, (s,))
s.run()
