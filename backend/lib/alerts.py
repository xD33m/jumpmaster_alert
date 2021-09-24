import json
import requests
import os
from playsound import playsound
from random import randrange
from lib.utils import getEnvId, resource_path


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


def playRandomSound():
    randomIndex = randrange(8)  # 0-7
    soundToPlay = resource_path(f'sounds\\voice{randomIndex+1}.wav')
    playsound(soundToPlay)
