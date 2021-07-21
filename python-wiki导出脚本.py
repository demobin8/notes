```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests
import os
import time
from urllib import parse
from pyquery import PyQuery as pq
import re
import fire
def generateHeaders():
    headersBrower = '''
Accept:application/json, text/javascript, */*; q=0.01
Accept-Encoding:gzip, deflate, sdch
Accept-Language:en-US,en;q=0.8
Connection:keep-alive
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 OPR/44.0.2510.857
    '''
    headersMap = dict()
    for item in headersBrower.splitlines():
        item = str.strip(item)
        if item and ":" in item:
            (key, value) = item.split(":", 1)
            headersMap[str.strip(key)] = str.strip(value)
    return headersMap
# 如果wiki需要登录验证,先用浏览器访问wiki,登录以后,获取该用户的cookie信息. cookie信息一般包含JSESSIONID
def genereateCookies():
    cookieString = "confluence.browse.space.cookie=space-blogposts; seraph.confluence=76939438%3A2dcdc324f8d1cf7105a3d53a9f3349d835e6308e; JSESSIONID=51F676DE3C05CF4DD43F57EE07C4D50A"
    cookieMap = {}
    for item in cookieString.split(";"):
        item = str.strip(item)
        if item and "=" in item:
            (key, value) = item.split("=", 1)
            cookieMap[str.strip(key)] = str.strip(value)
    return cookieMap
def save_file(url, path):
    if os.path.exists(path):
        logging.debug("exist path=" + path)
        return
    logging.debug("将 %s 保存到 %s" % (url, path))
    resp = requests.get(url, timeout=1000, headers=generateHeaders(), cookies=genereateCookies(), stream=True, verify=False)
    if resp.status_code  == 200:
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
        time.sleep(3)
    else:
        print("error ", resp.status_code)
def parse_host_pageId_fromurl(url):
    r = parse.urlparse(url)
    return r.scheme + '://' + r.netloc, parse.parse_qs(r.query, True)['pageId'][0]
def get_sub_pages_url(parentUrl):
    host, pageId = parse_host_pageId_fromurl(parentUrl)
    url = "%s/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&expandCurrent=false&hasRoot=true&pageId=%s&treeId=0&startDepth=0" % (host, pageId)
    resp = requests.get(url, timeout=1000, headers=generateHeaders(), cookies=genereateCookies(), stream=True,verify=False)
    if resp.status_code == 200:
        doc = pq(resp.text)
        links = []
        for a in doc.find("a").items():
            text = a.text().strip()
            if a.attr("href") and text:
                href = parse.urljoin(parentUrl, a.attr("href"))
                if href == parentUrl:
                    continue
                links.append({
                    "title" : text.encode("utf-8"),
                    "href" : href
                })
        return links
    else :
        logging.error("failed get url %s status_code=%d " % (url, resp.status_code))
    return []
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def export_wiki(url, name, dir='./doc'):
    if not os.path.exists(dir):
        os.makedirs(dir)
    restr = '/pages/viewpage.action'
    if(parse.urlparse(url).path != restr):
        print('url not valid' + url)
        return
    print("导出:",url)
    export_url = "%s/exportword?pageId=%s" % parse_host_pageId_fromurl(url)
    name = validateTitle(name)
    save_file(export_url, dir + "/" + name.replace('/','／') + ".doc")
    subpages = get_sub_pages_url(url)
    if subpages :
        parentdir = dir + "/" + name
        for subpage in subpages :
            export_wiki(subpage["href"], str(subpage["title"],encoding = "utf8"), parentdir)
if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    fire.Fire(export_wiki)
```
