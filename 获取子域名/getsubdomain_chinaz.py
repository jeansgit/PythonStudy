#!/usr/bin/python
# -*- coding:utf-8-*-
#Author:Jean 
import sys
import requests 
import re 
def getdomain(domain):
	url = "http://tool.chinaz.com/subdomain/"
	param = {'domain':'%s'%domain,'page':'1'}
	data = requests.post(url,data=param)
	r = re.findall('<a href="(http://\S+%s)'%domain,data.content)
	i = 1
	domain_http=[]
	while True:
		if len(r)==0:											#data为空则结束循环
			break
		url = "http://tool.chinaz.com/subdomain/"
		param = {'domain':'%s'%domain,'page':'%s'%i}
		data = requests.post(url,data=param)
		r = re.findall('<a href="(http://\S+%s)'%domain,data.content)
		for j in range(len(r)):
			domain_http.append(r[j])
			#print r[j]
		i = i+1 
	return 	list(set(domain_http))#去重
if __name__=="__main__":
	print "使用方法:	python getsubdomain_chinaz.py baidu.com".decode("utf-8")
	print "\n\n"
	target = sys.argv[1]
	file1 = open("%s-http.txt"%target,"w")
	domain_http = getdomain(target) 
	for i in range(len(domain_http)):
		file1.write(domain_http[i]+'\n')
	print "执行成功!".decode("utf-8")
	file1.close()