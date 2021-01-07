#!/usr/bin/python
#coding:utf-8
from bs4 import BeautifulSoup
import requests
import re
import time 
from optparse import OptionParser 
from fake_useragent import UserAgent

def GetOptions():
    optParser = OptionParser()
    optParser.add_option('-d','--domain',action = 'store',type = "string" ,dest = 'domain',help='Domain')
    optParser.add_option('-p','--page',action = 'store',type = "string" ,dest = 'page',help='page')
    (options, args) = optParser.parse_args() 
    return (options,args)

def GetHeaders():
    ua = UserAgent()
    header ={
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"%s"%ua.random,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate",
        "Accept-Language":"zh-CN,zh;q=0.9"
        }
    return header

def GetDomainFromBaidu(domain,page,filename):
    print("#######################################################Baidu##########################\n")
    result=[]
    file=open(filename,"w+")
   
    for j in range(1,page+1):
        p=(j-1)*10
        url="https://www.baidu.com/s?wd=site%%3A%s&pn=%s&oq=site%%3A%s\
        &ie=utf-8&fenlei=256&rsv_idx=1&rsv_pq=ee5b2a33000815e7&\
        rsv_t=685afsrI5MwzKqY7Q54co3Z4umvdAM0BApUIv7IX%%2B761hYc1O8%%2FyMog2fXk&rsv_page=1" %(domain,p,domain)
        print("获取site:%s第%s页的内容.................................."%(domain,j))
        
        data=requests.get(url=url,headers=GetHeaders())
        #print(data.text)
        soup=BeautifulSoup(data.text,'lxml')
        #print(soup)
        #tag=soup.find_all('div',attrs={'id':'content_left'})
        tag=soup.find_all('a',attrs={'class':'c-showurl c-color-gray'})
        #print(tag)
        for i in tag:
            #print(i)
            #print(i.string)
            getdomain=str(i.string).split('/')[0]
            if domain in getdomain:
                print(getdomain)
                if getdomain not in result:
                    result.append(getdomain)
                    file.write(getdomain+'\n')
        time.sleep(3)
    #print(result)
    file.close()
    return result

def GetDomainFromBing(domain,page,filename):
    print("#######################################################Bing##########################\n")
    result=[]
    file=open(filename,"w+")
    ua = UserAgent()
    for j in range(1,page+1):
        p=(j-1)*10
        print("获取site:%s第%s页的内容.................................."%(domain,j))
        url="https://cn.bing.com/search?q=site%%3a%s&qs=n&\
        sp=-1&pq=site%%3a%s&sc=1-14&sk=&cvid=F13445D401B348\
        2FBAF018C1403CDFC4&first=%s&FORM=PORE" %(domain,domain,p)
        #print(url)
        data=requests.get(url=url,headers=GetHeaders())
        #print(data.text)
        soup=BeautifulSoup(data.text,'lxml')
        #print(soup)
        #tag=soup.find_all('div',attrs={'id':'content_left'})
        tag=soup.findAll('h2')
        #print(tag)
        for i in tag:
            if i.a:
                print(i.a.get('href').split('/')[2])
                if domain in str(i.a.get('href').split('/')[2]):
                    if str(i.a.get('href').split('/')[2]) not in result:
                        result.append(str(i.a.get('href').split('/')[2]))
                        file.write(str(i.a.get('href').split('/')[2])+"\n")

        time.sleep(3)
    #print(result)
    file.close()
    return result

def GetDomainFrom360(domain,page,filename):
    print("#######################################################360##########################\n")
    result=[]
    file=open(filename,"w+")
    ua = UserAgent()
    for j in range(1,page+1):
        p=(j-1)*10
        url="https://www.so.com/s?q=site%%3A%s&pn=%s&psid=001266ee55b3cd61dbc2c072b5e8820a&src=srp_paging&fr=none" %(domain,p)
        print("获取site:%s第%s页的内容.................."%(domain,j))
        
        #s=requests.Session()
        data=requests.get(url=url,headers=GetHeaders())
        #print(data.text)
        soup=BeautifulSoup(data.text,'lxml')
        #print(soup)
        #tag=soup.find_all('div',attrs={'id':'content_left'})
        tag=soup.find_all('p',attrs={'class':'g-linkinfo'})
        #print(tag)
        for i in tag:
            #print(i)
            #print(i.cite.string)
            if '/' in i.cite.string:
                getdomain=i.cite.string.split('/')[0]
                print(getdomain)
            elif '>' in i.cite.string:
                getdomain=i.cite.string.split('>')[0]
                print(getdomain)
            else:
                getdomain=i.cite.string
            if domain in getdomain:
                print(getdomain)
                if getdomain not in result:
                    result.append(getdomain)
                    file.write(getdomain+'\n')
        time.sleep(3)
    print(result)
    file.close()

if __name__=="__main__":
    domainresult=[]
    baiduresult=[]
    bingresult=[]
    result360=[]
    (options,args)=GetOptions()
    file=open("Subdomain_%s.txt"%options.domain,"w+")
    try:
        baiduresult=GetDomainFromBaidu('%s'%options.domain,int(options.page),'%s_Baidu.txt'%options.domain)
        bingresult=GetDomainFromBing('%s'%options.domain,int(options.page),'%s_Bing.txt'%options.domain)
        result360=GetDomainFrom360('%s'%options.domain,int(options.page),'%s_360.txt'%options.domain)
        #print(baiduresult)
        #print(bingresult)
        if result360:
            domainresult=baiduresult+bingresult+result360
        else:
            domainresult=baiduresult+bingresult

    except Exception as e:
        print(e)
    domainresult=list(set(domainresult))
    #domainresult=list(set(domainresult)).sort()
    print(domainresult)
    
    for k in domainresult:
        file.write(k+"\n")
    file.close()