import json
import requests
import time
import sched
import mss
import numpy
import cv2
import os
from dotenv import load_dotenv
load_dotenv()


# https://stackoverflow.com/a/474543
s = sched.scheduler(time.time, time.sleep)
currentIteration = 0


def getEnvId():
    userId = os.getlogin()

    if userId == "juliu":
        return "JULIUS_ID"
    elif userId == "lucas":
        return "LUCAS_ID"


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


def image_comp(mon, imgToCompare):
    sct = mss.mss()

    img = numpy.asarray(sct.grab(mon))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, imgToCompare, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # cv2.imshow("Image", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('Fenster wird geschlossen')
    return max_val


def detect_jumpmaster(sc):
    global currentIteration
    maxIteration = 120

    name = './images/jumpIcon.png'
    jumpmasterIcon = cv2.imread(name, 0)

    # position of jumpmaster icon for 2560x1440 screens
    iconPosition = {'left': 1100, 'top': 1076, 'width': 80, 'height': 80}
    max_val = image_comp(iconPosition, jumpmasterIcon)
    print(f"jumpmaster: {max_val}")

    event = s.enter(1, 1, detect_jumpmaster, (sc,))
    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        sendDiscordDM("DU BIST JUMPASTER DU NOOB")
        s.cancel(event)
        detect_champion_selection(sc)
        currentIteration = 0
    elif(currentIteration == maxIteration):
        s.cancel(event)
        detect_champion_selection(sc)
        currentIteration = 0


def detect_champion_selection(sc):
    name = './images/bloodIcon.png'
    bloodIcon = cv2.imread(name, 0)

    # position of bloodhound icon for 2560x1440 screens
    iconPosition = {'left': 1509, 'top': 435, 'width': 70, 'height': 70}
    max_val = image_comp(iconPosition, bloodIcon)
    print(f"character selection: {max_val}")

    event = s.enter(20, 1, detect_champion_selection, (sc,))
    if max_val >= 0.8:
        s.cancel(event)
        detect_jumpmaster(sc)


s.enter(1, 1, detect_champion_selection, (s,))
s.run()
