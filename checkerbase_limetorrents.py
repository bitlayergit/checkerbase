import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tryLogin(data, proxy):
	email, password = data

	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'DNT': '1',
	    'Connection': 'keep-alive',
	    'Referer': 'https://www.limetorrents.info/home/?a=2',
	    'Upgrade-Insecure-Requests': '1',
	    'TE': 'Trailers',
	}

	data = {
	  'email': email,
	  'password': password,
	  'sublogin': '1',
	  'remember': '1'
	}

	response = requests.post('https://www.limetorrents.info/process.php', headers=headers, data=data, verify=False)
	if "?a=1" in response.url:
		return (True,"")

	return (False,)
