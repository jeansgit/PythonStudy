#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys,os
domain = sys.argv[1]
#print domain
domain1 = domain.split('.')[0]
domain2 = domain.split('.')[1]
#print domain1
f = open("%s-pass.txt"%domain1,"w")
for i in range(10):
	f.write(domain1+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'!'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'!'+'20'+str(i)+'\n')
	
	
for i in range(10):
	f.write(domain1+'@'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'@'+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'#'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'#'+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'!@#'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'!@#'+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'!@'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'!@'+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'@#'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'@#'+'20'+str(i)+'\n')		
	
for i in range(10):
	f.write(domain1+'#@'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'#@'+'20'+str(i)+'\n')		
	
for i in range(10):
	f.write(domain1+'!#'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'!#'+'20'+str(i)+'\n')
	
for i in range(10):
	f.write(domain1+'#!'+'200'+str(i)+'\n')
for i in range(10,18):
	f.write(domain1+'#!'+'20'+str(i)+'\n')
	
	
	
for i in range(10):
	f.write(domain1+str(i)+'\n')
f.write(domain1+'12'+'\n')
f.write(domain1+'123'+'\n')
f.write(domain1+'1234'+'\n')
f.write(domain1+'12345'+'\n')
f.write(domain1+'123456'+'\n')
f.write(domain1+'1234567'+'\n')
f.write(domain1+'12345678'+'\n')
f.write(domain1+'123456789'+'\n')
f.write(domain1+'66'+'\n')
f.write(domain1+'666'+'\n')
f.write(domain1+'6666'+'\n')
f.write(domain1+'66666'+'\n')
f.write(domain1+'666666'+'\n')
f.write(domain1+'6666666'+'\n')
f.write(domain1+'66666666'+'\n')
f.write(domain1+'666666666'+'\n')
f.write(domain1+'88'+'\n')
f.write(domain1+'888'+'\n')
f.write(domain1+'8888'+'\n')
f.write(domain1+'88888'+'\n')
f.write(domain1+'888888'+'\n')
f.write(domain1+'8888888'+'\n')
f.write(domain1+'88888888'+'\n')
f.write(domain1+'888888888'+'\n')
f.write(domain1+'@'+'123'+'\n')
f.write(domain+'\n')
f.write(domain1+'@'+domain2+'\n')
f.write(domain1+'@'+'.'+domain2+'\n')

print u"生成密码 ^__^"
f.close()