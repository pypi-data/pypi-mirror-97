import requests
from .http import Http

class Util:
	def login(self, token):
		url = "https://avatar.roblox.com/v1/avatar/set-player-avatar-type"
		token_header = {'X-CSRF-TOKEN': token}

		r = requests.post(url, headers = token_header, json = {"playerAvatarType": "R6"})

		print(r)