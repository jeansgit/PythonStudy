#!/usr/bin/python
# -*- coding:utf-8-*-
#Author:Jean 
import sys
import requests 
import re 
def getdomain(domain):
	data = requests.get("http://i.links.cn/subdomain/?b2=1&b3=1&b4=1&domain=%s"%domain)
	r = re.findall('<a href="(http://\S+%s)'%domain,data.content)
	domain_http = []
	for j in range(len(r)):
		domain_http.append(r[j])
		print r[j]
	return 	list(set(domain_http))#去重
if __name__=="__main__":
	print "使用方法:	python getsubdomain_links.py baidu.com".decode("utf-8")
	print "\n\n"
	target = sys.argv[1]
	file1 = open("%s-http.txt"%target,"w")
	domain_http = getdomain(target) 
	for i in range(len(domain_http)):
		file1.write(domain_http[i]+'\n')
	print "执行成功!".decode("utf-8")
	file1.close()