from .http import Http
import json

# Group Object
class Group:
    Name = None
    Id = None
    Owner = None
    OwnerName = None
    OwnerId = None
    EmblemUrl = None
    Description = None
    Roles = None
    
    def __init__(self, data):
        self.Name = data["Name"]
        self.Id = data["Id"]
        self.Owner = data["Owner"]
        self.OwnerName = data["Owner"]["Name"]
        self.OwnerId = data["EmblemUrl"]
        self.EmblemUrl = data["EmblemUrl"]
        self.Description = data["Description"]
        self.Roles = data["Roles"]

class Groups:
    def getGroupList(userid):
        res = Http.sendRequest("https://api.roblox.com/users/" + str(userid) + "/groups")
        return res

    def getGroup(groupid):
        res = Http.sendRequest("https://api.roblox.com/groups/" + str(groupid))
        res_decoded = res.decode("utf-8")
        res_loads = json.loads(res_decoded)
        return Group(res_loads)

    def getGroupAllies(groupid):
        res = Http.sendRequest("https://api.roblox.com/groups/" + str(groupid) + "/allies")
        return res

    def getGroupEnemies(groupid):
        res = Http.sendRequest("https://api.roblox.com/groups/" + str(groupid) + "/enemies")
        return res

    def getGroupRoles(groupid):
        res = Http.sendRequest("https://groups.roblox.com/v1/groups/" + str(groupid) + "/roles")
        return res