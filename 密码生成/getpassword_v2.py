#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys

domain = sys.argv[1]					#输入域名
n = 0									#域名中.的数量
for i in domain:
	if i == '.':
		n = n+1

domain_name = domain.split('.')[n-1]	#获取根域名
com = domain.split('.')[n]				#根域 .com / .cn
file1 = open("%s_password.txt"%domain_name,"w")
file2 = open("pass.txt","r")			#常用密码收集
lines = file2.readlines()
for line in lines:
	file1.write(line)					#常用密码写入最终的字典文件
file1.write('\n')

year = 1970
#特殊字符
char = ['','`','~','!','@','#','$','%','^','&','*','(',')','-','=','_',
'+',',','.','/',';','\\','\'','"','<','>','?','|',':','[',']','{','}',
'!@','!#','@#','@!','#@','#!','!@#','!#@','#@!','#!@','@!#','@#!','!@#$',
'!@#$%','!@#$%^','!@#$%^&','!@#$%^&*','!@#$%^&*(','!@#$%^&*()']

#数字串
num = ['1','12','123','1234','12345','123456','1234567','12345678',
'123456789','987654321','87654321','7654321','654321','54321','4321',
'321','21','6','66','666','6666','66666','666666','6666666','66666666',
'8','88','888','8888','88888','888888','8888888','88888888','0','00',
'000','0000','00000','000000','0000000','00000000']	

for i in range(49):						#1970年-2018年
	for j in char:								
		file1.write(domain_name+j+str(year+i)+'\n')	#baidu!2018
	for k in char:
		file1.write(str(year+i)+k+domain_name+'\n')	#2018@baidu			

for i in char:
	file1.write(domain_name+i+com+'\n')				#baidu.com

for i in num:
	file1.write(domain_name+i+'\n')					#baidu123

for i in num:
	file1.write(i+domain_name+'\n')					#123baidu

for i in char:
	for j in num:
		file1.write(domain_name+i+j+'\n')			#baidu@123
for i in char:
	for j in num:
		file1.write(j+i+domain_name+'\n')			#123@baidu
print u'成功生成特定密码，祝你爆破成功！'
file1.close()
file2.close()