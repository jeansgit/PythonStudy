#!/usr/bin/python 
#-*- coding=utf-8 -*-
f = open("ip.txt","r")
f2 = open("result.txt","w")
for i in f.readlines():
	ip = i.strip('\n').split('/')[0]
	ip0 = ip.split('.')[0] 
	ip1 = ip.split('.')[1] 
	ip2 = ip.split('.')[2] 
	ip3 = ip.split('.')[3] 
	ip_three = ip0+'.'+ip1+'.'+ip2
	num=i.strip('\n').split('/')[1]
	number = pow(2,32-int(num))-2
	for j in range(number):
		print ip_three+'.'+str(int(ip3)+j+1)
		result_ip = ip_three+'.'+str(int(ip3)+j+1)
		f2.write(result_ip+'\n')
f.close()
f2.close()