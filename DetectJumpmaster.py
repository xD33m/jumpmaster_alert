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
maxTries = 0
delayInSeconds = 0.5


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
    return max_val


def detect_jumpmaster(sc):
    global maxTries

    name = './images/jumpIcon.png'
    jumpmasterIcon = cv2.imread(name, 0)

    # position of jumpmaster icon for 2560x1440 screens
    mon = {'left': 1100, 'top': 1076, 'width': 80, 'height': 80}
    max_val = image_comp(mon, jumpmasterIcon)
    print(max_val)
    # cv2.imshow("Image", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('Fenster wird geschlossen')
    maxTries = maxTries + 1
    if max_val >= 0.8:
        sendDiscordDM("DU BIST JUMPASTER DU NOOB")
        s.enter(20, 1, detect_champion_selection, (sc,))
    elif maxTries == 120:
        s.enter(20, 1, detect_champion_selection, (sc,))
        maxTries = 0


def detect_champion_selection(sc):
    name = './images/bangIcon.png'
    bangaloreIcon = cv2.imread(name, 0)

    # position of bangalore icon for 2560x1440 screens
    mon = {}
    max_val = image_comp(mon, bangaloreIcon)
    print(max_val)
    if max_val >= 0.8:
        s.enter(1, 1, detect_jumpmaster, (sc,))


s.enter(delayInSeconds, 1, detect_jumpmaster, (s,))
s.run()
