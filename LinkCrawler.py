import sys
import time
import random
import requests
import re
from urlparse import urlparse, urlunparse
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def banner():
	print("""
=========================================================================
=========================================================================
          _______                      _____  _                 
         |__   __|                    |  __ \| |                
            | |_ __ _   _  ___   ___  | |__) | |__   __ _ _ __  
            | | '__| | | |/ _ \ / __| |  ___/| '_ \ / _` | '_ \ 
            | | |  | |_| | (_) | (__  | |    | | | | (_| | | | |
            |_|_|   \__,_|\___/ \___| |_|    |_| |_|\__,_|_| |_|
                                                       
 [+] Facebook: https://www.facebook.com/292706121240740
 [+] Github:   https://github.com/truocphan
 [+] Discord:  https://discord.gg/fuBe3af
 [+] Gmail:    truocphan112017@gmail.com
 [+] Youtube:  https://www.youtube.com/channel/UCtQSQrgAQSTKdvsEzrfpBzQ

=========================================================================
=========================================================================
""")


def extract_URL(url):
	try:
		Regex = "(href|src|srcset|action|data)[\t\s]*=[\t\s]*['\"]?([^ '\">]+)['\"]?"

		headers["User-Agent"] = user_agents[random.randrange(len(user_agents))]
		res = s.get(url, headers=headers, proxies=proxies, verify=False, allow_redirects=False)
		print("(" + str(urls.index(url)+1) + ") " + url + " (" + str(res.status_code) + ")")
		
		if res.status_code == 200:
			f = open(filename + ".txt", "a+")
			f.write(url + "\n")
			f.close()
		f = open(filename + ".log", "a+")
		f.write("[{}] {} ({})\n".format(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(time.time())), url, str(res.status_code)))
		f.close()


		for i in list(set(re.findall(Regex, res.text, flags=re.IGNORECASE))):
			url_parse = urlparse(i[1])
			if (url_parse.netloc == '' or url_parse.netloc == urlparse(url).netloc) and url_parse.scheme in ['', 'http', 'https']:
				if url_parse.scheme == '':
					url_parse = url_parse._replace(scheme=urlparse(url).scheme)
				if url_parse.netloc == '':
					url_parse = url_parse._replace(netloc=urlparse(url).netloc)
				if url_parse.path[0] != '/':
					url_parse = url_parse._replace(path=("/".join(urlparse(url).path.split("/")[:-1]) + "/" + url_parse.path))

				if urlunparse(url_parse) not in urls:
					urls.append(urlunparse(url_parse))
	except Exception as e:
		pass



if __name__ == "__main__":
	banner()
	headers = dict()
	proxies = dict()
	if len(sys.argv) == 2:
		proxies['http'] = ''
		proxies['https'] = ''
	elif len(sys.argv) == 3:
		proxies['http'] = sys.argv[2]
		proxies['https'] = sys.argv[2]
	else:
		exit(""" Usage: python {scriptname} URL [Proxy Server]
 
 Examples:
	- python {scriptname} http://example.com http://127.0.0.1:8080 (with Proxy)
	- python {scriptname} http://example.com\n""".format(scriptname=sys.argv[0]))

	urls = [sys.argv[1]]
	filename = "urls_{}".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time())))

	user_agents = requests.get("https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt").text.split("\n")[:-1]
	s = requests.Session()
	for url in urls:
		extract_URL(url)

	print("""
 [+] Links Crawled: {filename}.txt
 [+] LOG: {filename}.log""".format(filename=filename))
