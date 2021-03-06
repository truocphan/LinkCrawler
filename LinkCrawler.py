import argparse
import os, sys
import time
import random
import requests
import re
from urlparse import urlparse, urlunparse
import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


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
		REGEX = "<[^<>]*(?:href|src|srcset|action|data)[\t\s]*=[\t\s]*['\"]?([^ '\"<>]+)['\"]?[^<>]*>"

		headers["User-Agent"] = user_agents[random.randrange(len(user_agents))]
		res = s.get(url, headers=headers, proxies=proxies, verify=False, allow_redirects=False)
		print("(" + str(urls.index(url)+1) + ") " + url + " (" + str(res.status_code) + ")")
		
		if res.status_code in [301, 302] and res.headers["Location"] not in urls:
			urls.append(res.headers["Location"])
		else:
			if res.status_code == 200:
				f = open(filename + ".txt", "a+")
				f.write(url + "\n")
				f.close()
			f = open(filename + ".log", "a+")
			f.write("[{}] {} (Status: {} {} | Content-Type: {})\n".format(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(time.time())), url, str(res.status_code), res.reason, res.headers["Content-Type"]))
			f.close()

			links_find = re.findall(REGEX, res.text, flags=re.IGNORECASE)

			links_find = list(set(links_find))
			for link in links_find:
				url_parse = urlparse(link)
				if (url_parse.netloc == '' or url_parse.netloc == urlparse(url).netloc) and url_parse.scheme in ['', 'http', 'https']:
					if url_parse.scheme == '':
						url_parse = url_parse._replace(scheme=urlparse(url).scheme)
					if url_parse.netloc == '':
						url_parse = url_parse._replace(netloc=urlparse(url).netloc)
					if url_parse.path != '' and url_parse.path[0] != '/':
						url_parse = url_parse._replace(path=("/".join(urlparse(url).path.split("/")[:-1]) + "/" + url_parse.path))

					if urlunparse(url_parse._replace(fragment="")) not in urls:
						urls.append(urlunparse(url_parse._replace(fragment="")))
	except Exception as e:
		print(e)



if __name__ == "__main__":
	dir_script = os.path.dirname(os.path.realpath(sys.argv[0]))
	if not os.path.isdir(os.path.join(dir_script, "RESULTS")):
		os.mkdir(os.path.join(dir_script, "RESULTS"))
	banner()
	parser = argparse.ArgumentParser(description="LinkCrawler ...")
	parser.add_argument("URL", help="URL need to crawl (E.g: http://example.com/)")
	parser.add_argument("--proxy", help="Forwarding HTTP requests via proxy (E.g: http://127.0.0.1:8080,...)")
	parser.add_argument("--headers", help="Adding or modifying headers on HTTP requests (E.g: --headers \"Authorization: ...\" [--headers \"Cookie: ...\" [...]])", default=[], action="append")
	parser.add_argument("--wordlist", help="Wordlist file for brute force url (Default: " + os.path.join(dir_script, "data", "wordlists.txt")+")", default=os.path.join(dir_script, "data", "wordlists.txt"))
	args = parser.parse_args()

	filename = os.path.join(dir_script, "RESULTS", "urls_{}".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))))
	f = open(os.path.join(dir_script, "data", "user-agents.txt"))
	user_agents = f.read().split("\n")
	f.close()

	urls = [args.URL]
	try:
		f = open(args.wordlist)
		content = f.read().split("\n")
		f.close
		[urls.append(urlunparse(urlparse(i)._replace(scheme=urlparse(args.URL).scheme)._replace(netloc=urlparse(args.URL).netloc)._replace(fragment=""))) for i in content if urlunparse(urlparse(i)._replace(scheme=urlparse(args.URL).scheme)._replace(netloc=urlparse(args.URL).netloc)._replace(fragment="")) not in urls]
	except Exception as e:
		exit(e)
	
	proxies = dict()
	proxies["http"] = args.proxy
	proxies["https"] = args.proxy
	headers = dict()
	for header in args.headers:
		headers[header.split(": ")[0]] = header.split(": ")[1]

	s = requests.Session()
	for url in urls:
		extract_URL(url)

	print("""
 [+] Links Crawled: {filename}.txt
 [+] LOG requests: {filename}.log""".format(filename=filename))
