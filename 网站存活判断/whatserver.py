# -*- coding:utf-8 -*-

import time
import os
import platform
import requests
import sys
import subprocess

from multiprocessing.dummy import Pool
from ip2Region import Ip2Region
from utils import *
#from whatweb import check_cms


class HTTP_HEADER:
    ACCEPT = "Accept"
    ACCEPT_CHARSET = "Accept-Charset"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_RANGE = "Content-Range"
    CONTENT_TYPE = "Content-Type"
    COOKIE = "Cookie"
    EXPIRES = "Expires"
    HOST = "Host"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    LAST_MODIFIED = "Last-Modified"
    LOCATION = "Location"
    PRAGMA = "Pragma"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    PROXY_CONNECTION = "Proxy-Connection"
    RANGE = "Range"
    REFERER = "Referer"
    SERVER = "Server"
    SET_COOKIE = "Set-Cookie"
    TRANSFER_ENCODING = "Transfer-Encoding"
    URI = "URI"
    USER_AGENT = "User-Agent"
    VIA = "Via"
    X_POWERED_BY = "X-Powered-By"


results = []
searcher = Ip2Region('db/ip2region.db')
identify = False


def check_waf(headers):
    retval = re.search(r"wangzhan\.360\.cn", headers.get("X-Powered-By-360wzb", ""), re.I) is not None
    if retval:
        return "360"
    retval = re.search(r"\AAL[_-]?(SESS|LB)=", headers.get("SET-COOKIE", ""), re.I) is not None
    if retval:
        return "airlock"
    retval = re.search(r"MISS", headers.get("X-Powered-By-Anquanbao", ""), re.I) is not None
    if retval:
        return "anquanbao"
    retval = re.search(r"fhl", headers.get("X-Server", ""), re.I) is not None
    retval |= re.search(r"yunjiasu-nginx", headers.get("Server", ""), re.I) is not None
    if retval:
        return "baidu"
    retval = re.search(r"\Abarra_counter_session=", headers.get("SET-COOKIE", ""), re.I) is not None
    retval |= re.search(r"(\A|\b)barracuda_", headers.get("SET-COOKIE", ""), re.I) is not None
    if retval:
        return "barracuda"
    retval = headers.get("X-Cnection", "").lower() == "close"
    retval |= re.search(r"\ATS[a-zA-Z0-9]{3,6}=", headers.get(HTTP_HEADER.SET_COOKIE, ""), re.I) is not None
    retval |= re.search(r"BigIP|BIGipServer", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    retval |= re.search(r"\AF5\Z", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    if retval:
        return "bigip"
    retval = re.search(r"cloudflare-nginx", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    if retval:
        return "cloudflare"
    retval = re.search(r"jiasule-WAF", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    retval |= re.search(r"__jsluid=", headers.get(HTTP_HEADER.SET_COOKIE, ""), re.I) is not None
    retval |= re.search(r"jsl_tracking", headers.get(HTTP_HEADER.SET_COOKIE, ""), re.I) is not None
    # retval |= re.search(r"static\.jiasule\.com/static/js/http_error\.js", page or "", re.I) is not None
    if retval:
        return "jiasule"
    retval = re.search(r"NSFocus", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    if retval:
        return "nsfocus"
    retval = re.search(r"Safe3WAF", headers.get(HTTP_HEADER.X_POWERED_BY, ""), re.I) is not None
    retval |= re.search(r"Safe3 Web Firewall", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    if retval:
        return "safe3"
    retval = re.search(r"WAF/2\.0", headers.get(HTTP_HEADER.X_POWERED_BY, ""), re.I) is not None
    retval |= re.search(r"Safedog", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    retval |= re.search(r"safedog", headers.get(HTTP_HEADER.SET_COOKIE, ""), re.I) is not None
    if retval:
        return "safedog"
    retval = re.search(r"YUNDUN", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
    retval |= re.search(r"YUNDUN", headers.get("X-Cache", ""), re.I) is not None
    if retval:
        return "yundun"
    retval = re.search(r"aliyun|alicdn", headers.get('Set-Cookie', ""), re.I) is not None
    if retval:
        return "aliyun"
    return "No Waf"


def check_404(domain):
    path_404 = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16)))
    res = get_response("http://" + domain + '/' + path_404, 'get', 10)
    return res.status_code


def get_title(res):
    try:
        # res.encoding = 'utf-8'
        title = re.findall(r'<title>([^<]+)</title>', res.text)[0]
        return title.encode('utf8')
    except UnicodeEncodeError, e:
        res.encoding = 'utf8'
        title = re.findall(r'<title>([^<]+)</title>', res.text)[0]
        return title.encode('utf8')
    except Exception, e:
        return "No Title"


def checkServer(target):
    ping_str = "-n 4" if platform.system().lower() == "windows" else "-c 4"
    if len(target.split('\t')) == 2:
        domain = target.split('\t')[0]
        ip = target.split('\t')[1]
    else:
        domain = target
        ip = getipaddr(domain)
    try:
        if is_intra_ip(ip):
            results.append((domain, ip))
            return
        res = get_response("http://" + domain, 'get', 10)
        server = res.headers.get('Server', 'UnKnow')
        status_code = res.status_code
        title = get_title(res)
        length = res.headers.get('Content-Length', '0')
        if length == '0':
            length = len(res.text)
        lang = res.headers.get('X-Powered-By', '')
        set_cookie = res.headers.get('Set-Cookie', '')
        if lang == '':
            if 'ASPSESSIONID' in set_cookie:
                lang = 'asp'
            elif 'ASP.NET' in set_cookie:
                lang = 'asp.net'
            elif 'PHPSESSID' in set_cookie:
                lang = 'php'
            elif 'JSESSIONID' in set_cookie:
                lang = 'jsp'
            elif 'CFID' in set_cookie or 'CFTOKEN' in set_cookie:
                lang = 'cfm'
            else:
                lang = 'UnKnow'
        waf = check_waf(res.headers)
        if identify:
            cms = check_cms(domain)
        else:
            cms = ""
        if check_404(domain) == 200:
            friendly_404 = 'Yes'
        else:
            friendly_404 = 'No'
        print "%s\t%s" % (target, res.headers)
        if len(ip.split(', ')) > 1:
            for _ip in ip.split(', '):
                p = subprocess.Popen('ping ' + ping_str + " " + _ip, stdout=subprocess.PIPE)
                p.wait()
                if p.poll() == 0:
                    ping = "OK"
                else:
                    ping = "Faild"
                print "%s:%s" % (_ip, ping)
                results.append(
                    [domain, _ip, ping, status_code, length, title, server, waf, lang, cms, friendly_404])
        else:
            p = subprocess.Popen('ping ' + ping_str + " " + ip, stdout=subprocess.PIPE)
            p.wait()
            if p.poll() == 0:
                ping = "OK"
            else:
                ping = "Faild"
            print "%s:%s" % (ip, ping)
            results.append([domain, ip, ping, status_code, length, title, server, waf, lang, cms, friendly_404])
        time.sleep(0.01)
    except Exception, e:
        if len(ip.split(', ')) > 1:
            for _ip in ip.split(', '):
                p = subprocess.Popen('ping ' + ping_str + " " + _ip, stdout=subprocess.PIPE)
                p.wait()
                if p.poll() == 0:
                    ping = "OK"
                else:
                    ping = "Faild"
                print "%s:%s" % (_ip, ping)
                results.append([domain, _ip, ping, 0, 0, "", "", "", "", "", ""])
        else:
            p = subprocess.Popen('ping ' + ping_str + " " + ip, stdout=subprocess.PIPE)
            p.wait()
            if p.poll() == 0:
                ping = "OK"
            else:
                ping = "Faild"
            print "%s:%s" % (ip, ping)
            results.append([domain, ip, ping, 0, 0, "", "", "", "", "", ""])


def load_targets(target):
    targets = []
    with open('output/' + target + '.txt') as f:
        for line in f.readlines():
            # print line.strip()
            targets.append(line.strip())
    return targets


def save_results(target):
    with open('output/' + target + '_server.txt', 'w') as f:
        f.write("Domain\tIp\tPing\tStatus\tLength\tTitle\tServer\tWaf\tLang\tCMS\tFriendly404\tGeo\n")
        for result in results:
            ip = result[1]
            data = searcher.btreeSearch(ip)
            geo = "%s" % data["region"]
            result.append(geo)
            line = '\t'.join([str(x) for x in result])
            f.write(line + '\n')


def whatServer(target, threads_num):
    if os.path.isfile('output/' + target + '.txt'):
        pool = Pool(threads_num)
        pool.map(checkServer, load_targets(target))
        pool.close()
        pool.join()
        save_results(target)
    else:
        checkServer(target)
    searcher.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        target = sys.argv[1]
        cms_identify = sys.argv[2]
        if cms_identify == "1":
            identify = True
            whatServer(target, 10)
        elif cms_identify == "0":
            identify = False
            whatServer(target, 10)
        else:
            print ("usage: %s domain cms_identify=1|cms_identify=0" % sys.argv[0])
    else:
        print ("usage: %s domain cms_identify=1|cms_identify=0" % sys.argv[0])
        sys.exit(-1)
