#!usr/bin/python
# -*- coding:utf-8 -*-
import socket
import sys
import threading
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool #线程池别名:ThreadPool

socket.setdefaulttimeout(0.5)	#设置超时时间

url=sys.argv[1]					#获取要扫描的url或IP
ip=socket.gethostbyname(url)	#获取ip
ports=[]	#所有端口
file=open("%s_result.html"%url,"w")
file.write("<html>")
file.write("<body>")
file.write("<h1>主机%s端口扫描</h1>"%ip)
file.write("<table>")
file.write("<tr>")
#file.write("<th>Host</th>")
file.write("<th>Port</th>")
file.write("<th>Banner</th>")
file.write("</tr>")
print "Start Scanning the host: %s"%url
print '-'*100
def scanport(port):
	
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		data=s.connect_ex((ip,port))	#功能与connect(address)相同，但是成功返回0，失败返回errno的值。
		if data==0:				#为0则成功
			try:
				s.send("Iwanttoscanport")
				banner=s.recv(1024)
			except Exception,e:
				print "The port %s is Open"%format(port)
				file.write("<tr>")
				file.write("<td>%s</td>"%format(port))
				file.write("<td>None</td>")
				file.write("</tr>")
				print str(e.message)
			else:
				print "The port %s is Open"%format(port)
				file.write("<tr>")
				file.write("<td>%s</td>"%format(port))
				file.write("<td>%s</td>"%format(banner))
				file.write("</tr>")
		s.close()

	except socket.gaierror:
		print "hostname error"
	except socket.error:
		print "connect error"
		
for i in range(1,65535):
	ports.append(i)
t1=datetime.now()
pool=ThreadPool(processes=1024)
pool.map(scanport,ports)
pool.close()
pool.join()
file.write("</table>")
file.write("</body>")
file.write("</html>")
file.close()
t2=datetime.now()
totaltime=t2-t1
print u"耗时%s"%totaltime