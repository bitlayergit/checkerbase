import js2py
import requests
import time

def auth_cloudflare(domain):
	if ss == None:
		ss = requests.session()
	headers = {
	    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'referer': 'https://'+domain+'/',
	    'accept-language': 'en-US,en;q=0.9',
	}
	resp = ss.get("https://{}/".format(domain), headers=headers).text
	s = resp.split('name="s" value="')[1].split('"')[0]
	jschl = resp.split('name="jschl_vc" value="')[1].split('"')[0]
	formpass = resp.split('name="pass" value="')[1].split('"')[0]
	js = resp.split('setTimeout(function(){')[1].split('f.action += location.hash;')[0]
	js = js.split("t = document.createElement('div');")[0] + "t = '"+domain+"';" + js.split("('challenge-form');")[1]
	js = js.replace('a.value = ','return ')
	js = "function work(){ " + js + " } work();"
	answer = js2py.eval_js(js)
	params = (
	    ('s', s),
	    ('jschl_vc', jschl),
	    ('pass', formpass),
	    ('jschl_answer', str(answer)),
	)
	time.sleep(4)
	resp = ss.get("https://"+domain+"/cdn-cgi/l/chk_jschl", headers=headers, params=params)
	return ss.cookies

# Example use:
# print(auth_cloudflare("itorrents.org"))
# Returns (Requests.sessions.Session, RequestsCookieJar)
# Can be used like: requests.get(...., cookies=auth_cloudflare(...))
