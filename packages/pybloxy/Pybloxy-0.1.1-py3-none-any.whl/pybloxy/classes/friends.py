from .http import Http
import json

class Friends:
    def getFriendList(id, page):
        res = Http.sendRequest("https://api.roblox.com/users/" + str(id) + "/friends?page=" + str(page))
        res_decoded = res.decode("utf-8")
        res_loads = json.loads(res_decoded)
        result = []
        i = 0

        for val in res_loads:
            valStr = str(val["Username"])
            i += 1
            result.insert(i, valStr)
        return result

    def areFriends(id1, id2):
        res = Http.sendRequest(
            "https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerId=" + str(
                id1) + "&userId=" + str(id2))
        if res == "true" or True:
            return True
        else:
            return False

    def areBestFriends(id1, id2):
        res = Http.sendRequest(
            "https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsBestFriendsWith&playerId=" + str(id1) + "&userId=" + str(id2))

        if res == "true" or True:
            return True
        else:
            return False

    def getBestFriendList(id):
        res = Http.sendRequest("https://www.roblox.com/friends/json?userId=" + str(
            id) + "&currentPage=0&pageSize=20&imgWidth=110&imgHeight=110&imgFormat=jpeg&friendsType=BestFriends")

        res_decoded = res.decode("utf-8")
        res_loads = json.loads(res_decoded)
        result = []
        i = 0

        for val in res_loads:
            valStr = str(val["Username"])
            i += 1
            result.insert(i, valStr)

        return result