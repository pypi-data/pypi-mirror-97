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
	# GETs

	def checkUsernameExists(self, username):
		potentialuser = self.getUser(username)

		if potentialuser.Username != "":
			return True
		else:
			return False

	
	def getUser(self, username):
		try:
			res = Http.sendRequest("https://api.roblox.com/users/get-by-username?username=" + str(username))
			res_decoded = res.decode("utf-8")
			res_loads = json.loads(res_decoded)

			return User(res_loads)
		except:
			return None

	def getBadges(self, id):
		res = Http.sendRequest(
			"https://www.roblox.com/badges/roblox?userId=" + str(id) + "&imgWidth=110&imgHeight=110&imgFormat=png")
		return res

	# User
	
	def getCurrency(self):
		res = Http.sendRequest

	# Util

	def login(token):
		Util.login(token)