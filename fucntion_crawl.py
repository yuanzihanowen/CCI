__author__ = 'zihanyuanowen'


import scrapy
import requests
import urllib2


if __name__ == '__main__':
    website = 'http://www.wallstreetoasis.com/#'
    # without the header, the request shows result access forbidden
    hdr = {'User-Agent': 'Mozilla/5.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    try:
        req = urllib2.Request(website, headers=hdr)
    except urllib2.urlError, e:
        print(e.reason)
    response = urllib2.urlopen(req)
    html = response.read()
    print(html)



