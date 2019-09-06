import requests
import time
import json

def tryLogin(data, proxy):
	username, password = data

	data = {
	  'username': username,
	  'password': password
	}

	response = requests.post('http://www.oddstorm.com/clientapp_live/login.php', data=data)
	if response.text == "1":
		return (True,"")
	else:
		return (False,)
