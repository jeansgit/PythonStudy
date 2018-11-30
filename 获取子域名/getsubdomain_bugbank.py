#!/usr/bin/python
# -*- coding:utf-8-*-
#Author:Jean 
import sys
import urllib2 
import re 
def getdomain(domain):
	url="http://www.bugbank.cn/api/subdomain/collect?domain=%s&page=1"%domain
	data = urllib2.urlopen(url).read()
	data_to_dic = eval(data)
	i = 1
	domain_subdomain=[]
	domain_http=[]
	domain_ip = []
	while True:
		if len(data_to_dic['data'])==0:			#data为空则结束循环
			break
		url="http://www.bugbank.cn/api/subdomain/collect?domain=%s&page=%d"%(domain,i) 
		data = urllib2.urlopen(url).read()	#获取网页内容
		data_to_dic = eval(data)					#强制将字符串转为字典
		data_domain_info = data_to_dic['data']				#取值 
		for j in range(len(data_domain_info)):
			domain_http.append(data_domain_info[j]['domain'])
			domain_ip.append(data_domain_info[j]['ips'][0])
			domain_subdomain.append(data_domain_info[j]['domain']+'      '+data_domain_info[j]['ips'][0])
		i = i+1 
	return list(set(domain_subdomain)),list(set(domain_http)),list(set(domain_ip))	#去重
if __name__=="__main__":
	print "使用方法:	python getsubdomain_bugbank.py baidu.com".decode("utf-8")
	print "\n\n"
	target = sys.argv[1]
	file1 = open("%s-subdomain.txt"%target,"w")
	file2 = open("%s-http.txt"%target,"w")
	file3 = open("%s-ip.txt"%target,"w")
	domain_subdomain,domain_http,domain_ip = getdomain(target) 
	for i in range(len(domain_subdomain)):
		file1.write(domain_subdomain[i]+'\n')
	for i in range(len(domain_http)):
		file2.write('http://'+domain_http[i]+'\n')
	for i in range(len(domain_ip)):
		file3.write(domain_ip[i]+'\n')
	print "执行成功!".decode("utf-8")
	file1.close()
	file2.close()
	file3.close()