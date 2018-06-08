from urllib.request import Request, urlopen
import json
import envVariables


def getCountOfUsersInDatahubChatRoom():
    GITTER_TOKEN = envVariables.GITTER_TOKEN
    url = 'https://api.gitter.im/v1/rooms/598aa900d73408ce4f70a21d?access_token=' + GITTER_TOKEN
    gitterResponse = urlopen(Request(url))
    gitterResponseJSON = json.loads(gitterResponse.read())
    userCount = gitterResponseJSON['userCount']
    return userCount
