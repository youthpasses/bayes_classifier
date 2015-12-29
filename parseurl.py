#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import urllib2
from bs4 import BeautifulSoup


def getTextFromUrl(url, index):
    if index > 0 and index < 7:
        return getText1_6(url)
    elif index == 7:
        return getText7(url)


def getText1_6(url):
    response = urllib2.urlopen(url)
    html = response.read()
    pattern = re.compile(r'<P style="TEXT-INDENT: 2em">(.*?)</P>')
    articlePs = re.findall(pattern, html)
    text = ''
    if len(articlePs) >= 1:
        for p in xrange(0, len(articlePs)):
            articleP = articlePs[p].decode('gbk').encode('utf-8')
            enPattern = re.compile(r'<.*?>')
            ens = re.findall(enPattern, articleP)
            if len(ens) > 0:
                for i in xrange(0, len(ens)):
                    articleP = articleP.replace(ens[i], "")
            text = text + articleP
    return text


def getText7(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    text_ = str(soup.find_all('div', id='artical_real'))
    pattern = re.compile(r'<p>(.*?)</p>')
    ps = re.findall(pattern, text_)
    text = ''
    if len(ps) != 0:
        #判断有几段p，不为零就记录
        for p in ps:
            #删除p中所有的<.*?>
            enPattern = re.compile(r'<.*?>')
            ens = re.findall(enPattern, p)
            if len(ens) > 0:
                for en in ens:
                    p = p.replace(en, '')
            text = text + p
    return text
