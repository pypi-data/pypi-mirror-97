from .http import Http
from .util import Util
import json

class User:
	Id = None
	Username = None
	AvatarUri = None
	AvatarFinal = None
	IsOnline = None
	
	def __init__(self,data):
		self.Id = data["Id"]
		self.Username = data["Username"]
		self.AvatarUri = data["AvatarUri"]
		self.AvatarFinal = data["AvatarFinal"]
		self.IsOnline = data["IsOnline"]

class Users:
	def checkUsernameExists(username):
		try:
			res = Http.sendRequest("https://www.roblox.com/UserCheck/DoesUsernameExist?username=" + str(username))
			res_decoded = res.decode("utf-8")
			res_loads = json.loads(res_decoded)

			if res_loads["success"] == "True" or True:
				return True
			else:
				return False
		except:
			return False

	def getUser(username):
		try:
			res = Http.sendRequest("https://api.roblox.com/users/get-by-username?username=" + str(username))
			res_decoded = res.decode("utf-8")
			res_loads = json.loads(res_decoded)

			return User(res_loads)
		except:
			return None

	def getBodyColors(id):
		res = Http.sendRequest("https://www.roblox.com/Asset/BodyColors.ashx?userId=" + str(id))
		return res

	def getAssetsWorn(id):
		res = Http.sendRequest("https://www.roblox.com/Asset/AvatarAccoutrements.ashx?userId=" + str(id))
		return res

	def getAssetVersions(id, placeid):
		res = Http.sendRequest(
			"https://www.roblox.com/Asset/CharacterFetch.ashx?userId=" + str(id) + "&placeId=" + str(placeid))
		return res

	def getPlaces(id):
		res = Http.sendRequest("https://www.roblox.com/Contests/Handlers/Showcases.ashx?userId=" + str(id))
		return res

	def getBadges(id):
		res = Http.sendRequest(
			"https://www.roblox.com/badges/roblox?userId=" + str(id) + "&imgWidth=110&imgHeight=110&imgFormat=png")
		return res
	
	# New Cmds

	def login(token):
		Util.login(token)