import logging
import requests

class Http:
	def sendRequest(url):
		payload = requests.get(str(url))
		statusCode = payload.status_code
		content = payload.content

		if statusCode != 200:
			return logging.error(f"[Roblox.py - GET] Something went wrong! Error Code: {statusCode}")
		
		return content

	def postRequest(url, payload):
		payload = requests.post(str(url), data = payload)
		statusCode = payload.status_code
		content = payload.content

		if statusCode != 200:
			return logging.error(f"[Roblox.py - POST] Something went wrong! Error Code: {statusCode}")
		
		return content
