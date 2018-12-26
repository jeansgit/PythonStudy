#!/usr/bin/python
# -*- coding:utf-8 -*- 
#Author: Jean
import requests
import sys
import socket
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout, ConnectionError, RequestException

def getbaidusubdomain(domain,page):
	resulturls=[]
	ips=[]
	for i in range(1,page):
		baidu_url="https://www.baidu.com/s?wd=site%%3A%s&pn=%d&oq=site%%3A%s&tn=baiduhome_pg&ie=utf-8&usm=1&rsv_idx=2&rsv_pq=86a866d2000d92fd&rsv_t=1ee5C4FU2EXcspZnUacDronj28QQpI363e4eUuQUUXMAyuROHkbT8adBhv9%%2BZ%%2B2GXVYA"%(domain,(i-1)*10,domain)
		bing_url="https://cn.bing.com/search?q=domain%%3a%s&go=%%E6%%8F%%90%%E4%%BA%%A4&qs=ds&first=%d&FORM=PERE"%(domain,(i-1)*10)
		print "获取百度搜索第%d页的子域名---------------------->".decode("utf-8")%i	
		#print baidu_url
		baidu_header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/5%d.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'%i}
		bing_header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/51.0.2661.102 UBrowser/6.1.2107.204 Safari/537.3%d'%i}
		#baidu_cookie={'Cookie':'BAIDUID=5EC12254A48A085D517FAA8174715AB9:FG=1; BDUSS=BpVWRtQTVrUkFMWlBjSC0ya1RzazF4Z1c0V2NUTVl6b1VxQ0wxbUNzRnV1MEpjQVFBQUFBJCQAAAAAAAAAAAEAAADy4R1SV09IRUxMTzkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG4uG1xuLhtcQT; BIDUPSID=5EC12254A48A085D517FAA8174715AB9; PSTM=1545285745; ispeed_lsm=2; BD_HOME=1; BD_UPN=12314353; sug=3; sugstore=0; ORIGIN=0; bdime=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_645EC=e99fUS%%2Br4x5R2qFack71mraEDg2kYD89HvOwvNB9y%%2FDXLiYeWm5fxrZ4zRvBYzP8Cibo; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=7; BDSVRTM=13%d; H_PS_PSSID=26524_1449_21111_28206_28132_27751_27245'%i}
		bing_cookie={'Cookie':'_EDGE_V=1; MUID=17070C6A3F486057249500A13E3761B8; MUIDB=17070C6A3F486057249500A13E3761B8; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=6623443BD2994CCBA40B04E2C351F373&dmnchg=1; ENSEARCH=BENVER=0; _EDGE_S=SID=1ACCCFD973C6668E3D41C30972E867F5; SRCHUSR=DOB=20181220&T=1545786397000; ipv6=hit=1545789997041&t=4; _SS=SID=1ACCCFD973C6668E3D41C30972E867F5&HV=1545787979; SRCHHPGUSR=CW=1581&CH=854&DPR=0.8999999761581421&UTC=480&WTS=6368138319%d'%i}
		try:
			baidu_html=requests.get(baidu_url,headers=baidu_header)
			bing_html=requests.get(bing_url,headers=bing_header,cookies=bing_cookie)
		except ReadTimeout:
			print "Timeout!"
		except ConnectionError:
			print "Connection Error!"
		except RequestException:
			print "Error!"
		baidu_soup=BeautifulSoup(baidu_html.content,"html.parser",from_encoding="utf-8")
		bing_soup=BeautifulSoup(bing_html.content,"html.parser",from_encoding="utf-8")
		baidu_items=baidu_soup.find_all('a',class_="c-showurl")
		bing_items=bing_soup.find_all('div',class_="b_attribution")
		for baidu_item in baidu_items:
			baidu_requrl=baidu_item.get("href")
			#print baidu_requrl
			requests.packages.urllib3.disable_warnings()
			baidu_data=requests.get(baidu_requrl,headers=baidu_header,verify=False)
			baidu_host=baidu_data.url.split('/')[2]
			print baidu_host
			resulturls.append(baidu_host)
			baidu_ip=socket.gethostbyname(baidu_host)
			ips.append(baidu_ip)
		print "获取必应搜索第%d页的子域名---------------------->".decode("utf-8")%i	
		#print bing_url
		for bing_item in bing_items:
			bing_requrl=bing_item.get_text()
			#print bing_requrl
			if ('/' in bing_requrl) and ('http' in bing_requrl):
				binghost=bing_requrl.split('/')[2]
				print binghost
			elif '/' in bing_requrl:
				binghost=bing_requrl.split('/')[0]
				print binghost
			else:
				binghost=bing_requrl
				print binghost
			resulturls.append(binghost)
			bing_ip=socket.gethostbyname(binghost)
			ips.append(bing_ip)
	seturls=list(set(resulturls))
	setips=list(set(ips))
	#print seturls
	resultdomain=open("%s_domain.txt"%domain,"w")
	for theurl in seturls:
		resultdomain.write(theurl+"\n")
	resultip=open("%s_ip.txt"%domain,"w")
	for theip in setips:
		resultip.write(theip+"\n")
	resultdomain.close()
	resultip.close()

if __name__=="__main__":
	print "使用方法:	python getsubdomain.py baidu.com page".decode("utf-8")
	print "\n\n"
	domain=sys.argv[1]
	page=int(sys.argv[2])+1
	getbaidusubdomain(domain,page)