#!/usr/bin/python
# -*- coding:utf-8 -*-  
import os,sys
def check_ip(ip):									#处理ip
	ip_addr = ip.split('.')
	if len(ip_addr) != 4:							#ip格式
		print u"小伙子，你IP格式不正确= ="
		sys.exit() 
	for i in range(4):		
		try:
			ip_addr[i] = int(ip_addr[i])			#int型
		except:
			print u"小伙子，你IP格式不正确= ="
		if  ip_addr[i]<=255 and ip_addr[i]>=0:		#ip的范围
			pass 
		else:
			print u"小伙子，你IP格式不正确= ="
			sys.exit()
		i = i+1 
	return ip_addr

def result_ip():									#得到结果ip
	file1 = open("result.txt","w")					#保存结果
	file2 = open("goal.txt","r")					#要扫的ip
	result = []
	for i in file2.readlines():						#逐行读取
		ip = check_ip(i.strip('\n'))
		ip_last = ip[3]
		ip_first = str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])	#ip前三位
		if ip_last>=250:
			for i in range(245,256):
				result.append(ip_first+'.'+str(i))	#ip拼接
		if ip_last<=5:
			for i in range(1,11):
				result.append(ip_first+'.'+str(i))	#ip拼接
		if ip_last>5 and ip_last<250:
			for i in range(ip_last-5,ip_last):
				result.append(ip_first+'.'+str(i))	#ip拼接
			for i in range(ip_last,ip_last+5):
				result.append(ip_first+'.'+str(i))	#ip拼接
	result = set(result)							#去重
	for i in result:
		print i 
		file1.write(i+'\n')							#写到文件
	file1.close()
	file2.close()
if __name__ == "__main__":
	result_ip()										#执行
	print "\n\n"
	print u"执行完毕"
	print "\n"