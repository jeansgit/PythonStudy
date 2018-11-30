import random
import re
import requests
import socket
from struct import unpack

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def random_useragent():
    return random.choice(USER_AGENTS)


def random_x_forwarded_for():
    return '.'.join(str(random.randint(1, 255)) for _ in range(4))


def get_response(url, method="get", timeout=10):
    try:
        res = ''
        headers = {'User-Agent': random_useragent(), 'X-Forwarded-For': random_x_forwarded_for()}
        if method == "head":
            res = requests.head(url, timeout=timeout, headers=headers)
        elif method == "get":
            res = requests.get(url, timeout=timeout, headers=headers, allow_redirects=False)
        elif method == "options":
            res = requests.options(url, timeout=timeout, headers=headers)
        return res
    except Exception, e:
        print e
        return


def get_html(url, timeout=10):
    try:
        headers = {'User-Agent': random_useragent(), 'X-Forwarded-For': random_x_forwarded_for()}
        return requests.get(url, timeout=timeout, headers=headers, allow_redirects=False).text
    except Exception, e:
        print e
        return ""


def getipaddr(hostname):
    trytime = 0
    while True:
        try:
            ipaddr = socket.getaddrinfo(hostname, 'http')[0][4][0]
            return ipaddr
        except:
            trytime += 1
            if trytime > 3:
                return ""


def is_domain(domain):
    m = re.match(r'(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', domain)
    return True if m else False


def is_ip(ip_str):
    ip_regx = """
            ^
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            \.
            (?:\d{1,2}|1\d\d|2[0-4]\d|25[0-5])
            $
        """
    result = True if re.search(ip_regx, ip_str, re.X) else False
    return result


def ip2long(ip_str):
    return unpack("!L", socket.inet_aton(ip_str))[0]


def is_intra_ip(ip_str):
    ip = ip2long(ip_str)
    return ip2long('127.0.0.0') >> 24 == ip >> 24 or \
           ip2long('10.0.0.0') >> 24 == ip >> 24 or \
           ip2long('172.16.0.0') >> 20 == ip >> 20 or \
           ip2long('192.168.0.0') >> 16 == ip >> 16
