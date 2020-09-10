# -*- coding: utf-8 -*-
#####################################
#   SCANNER WP-FILE-MANAGER-0DAY    #
#   Telegram = @h0d3_g4n            #
#   ICQ = @h0d3_g4n                 #
#   Skype = live:f2c962ccea77ec0    #
# code by h0d3_g4n thanks androxgh0s#
#####################################
import requests, os, sys,re
from urlparse import urlparse
from re import findall as reg
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue
from colorama import Fore                           
from colorama import Style
from colorama import init
init(autoreset=True)
class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try: func(*args, **kargs)
			except Exception, e: print e
			self.tasks.task_done()

class ThreadPool:
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		for _ in range(num_threads): Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		self.tasks.join()

def printf(text):
	''.join([str(item) for item in text])
	print(text + '\n'),

def main(url):
	try:
		text = '\033[32;1m#\033[0m '+url
		headers ={
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
		}
		get_jembut = requests.get(url+'/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php',headers=headers,timeout=15).content
		if '{"error":["errUnknownCmd"]}' in get_jembut:
			text += ' => \033[32;1mVuln !!!\033[0m'
			open('vuln.txt', 'a').write(url+'\n')
		else:
			text += ' => \033[31;1mNot Vuln\033[0m'
	except:
		text = '\033[31;1m#\033[0m '+url
		text += ' => \033[31;1mCan\'t access sites\033[0m'
	printf(text)

if __name__ == '__main__':
	print("""
 ___ ___ ___ __  _  __  _  _   _   _  __  ___  __   __  
| _,| __| _ |  \| |/  \| || | | | | |/  \| _ \/  \/' _/ 
| v_| _|| v | | ' | /\ | >< | | 'V' | /\ | v | /\ `._`. 
|_| |___|_|_|_|\__|_||_|_||_| !_/ \_|_||_|_|_|_||_|___/ 
	SCANNER \033[32;1mWP-FILE-MANAGER-0DAY\033[0m by h0d3_g4n \n""")
	try:
		lists = sys.argv[1]
		numthread = sys.argv[2]
		readsplit = open(lists).read().splitlines()
	except:
		try:
			lists = raw_input("Give Me List => ")
			readsplit = open(lists).read().splitlines()
		except:
			print("Wrong input or list not found!")
			exit()
		try:
			numthread = raw_input("threads => ")
		except:
			print("Wrong thread number!")
			exit()
	pool = ThreadPool(int(numthread))
	for url in readsplit:
		if "://" in url:
			url = url
		else:
			url = "http://"+url
		if url.endswith('/'):
			url = url[:-1]
		jagases = url
		try:
			pool.add_task(main, url)
		except KeyboardInterrupt:
			exit()
	pool.wait_completion()
