#!usr/bin/python
# -*- coding:utf-8 -*-
import requests
import sys 
from multiprocessing.dummy import Pool as ThreadPool #线程池别名

file1=open("url.txt","r")
scanurl=sys.argv[1]
name=scanurl.split('/')[-1]
file2=open("%s_webscan.html"%name,"w")
file2.write("<html>")
file2.write("<body>")
file2.write("<h1>%s目录扫描</h1>"%scanurl)
file2.write("<table>")
file2.write("<tr>")
file2.write("<th>存在路径</th>")
file2.write("</tr>")

def scan(url):
	header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
	#print url
	completeurl=scanurl+url
	print "Scanning %s.................................."%completeurl
	html=requests.get(completeurl,headers=header)
	#print html.url	#返回跳转后的url
	code=html.status_code
	#print code
	if code==200:
		if html.url==completeurl:
			print u"%s..................................存在"%completeurl
			file2.write("<tr>")
			file2.write("<td><a href=%s>%s</a></td>"%(completeurl,completeurl))
			file2.write("</tr>")

urls=[]			
for line in file1.readlines():
	url=line.strip('\n')
	urls.append(url)
try:	
	pool=ThreadPool(processes=1000)
	pool.map(scan,urls)
	pool.close()
	pool.join()
except:
	print "error"
file2.write("</table>")		
file2.write("</html>")
file2.write("</body>")
file2.close()
file1.close()