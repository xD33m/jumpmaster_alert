import json
import requests
import os
import winsound
from random import randrange
from lib.utils import getEnvId, resource_path
import time
soundActivated = False
discordDMActivated = False


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


def playRandomSound():
    randomIndex = randrange(1, 8)
    filename = "voice{}.wav".format(randomIndex)
    file = os.path.join('..', 'sounds', filename)
    soundToPlay = resource_path(file)
    winsound.PlaySound(soundToPlay, winsound.SND_FILENAME)


def updateNotificationSettings(variable, value):
    if variable == 'sound':
        global soundActivated
        soundActivated = value
    elif variable == 'discordDM':
        global discordDMActivated
        discordDMActivated = value
    else:
        print('Variable not found')


def sendNotification(message):
    if soundActivated:
        playRandomSound()
    if discordDMActivated:
        sendDiscordDM(message)
