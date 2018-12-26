#!/usr/bin/python
# -*- coding:utf-8 -*- 
#Author: Jean
import requests
import threading

from requests.exceptions import ReadTimeout, ConnectionError, RequestException


def getdic():
	dic=[]
	file=open("dict.txt","r")
	for i in file.readlines():
		dist=i.strip()
		#print dist
		url="http://"+dist+".baidu.com"
		dic.append(url)
	return dic

def brute(url):
	header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/51.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
	requests.packages.urllib3.disable_warnings()
	try:
		data=requests.get(url,headers=header,verify=False)
		if data.status_code==200:
			print url
	except ReadTimeout:
		print "Timeout!"
	except ConnectionError:
		print "Connection Error!"
	except RequestException:
		print "Error!"

for i in range(10000):
	dic=getdic()
	for url in dic:
		t=threading.Thread(target=brute,args=(url,))
		t.start()