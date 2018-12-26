#!/usr/bin/env python
# coding=utf-8
from HTMLParser import HTMLParser
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8" )
from collections import namedtuple



class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def HTmltoText(HtmlConntent):
    try:
        F = namedtuple('HtmlToText', ['status', "text","error"])
        parser = _DeHTMLParser()
        parser.feed(HtmlConntent)
        parser.close()
        return F._make([True,parser.text(),""])
    except Exception, e:
        return F._make([True, "",str(e)])


def TextToHtml(Conntent):
    try:
        F = namedtuple('TextToHtml', ['status', "text", "error"])
        HtmlHead = "<!DOCTYPE html><html><head lang='en'><meta charset='UTF-8'><title></title><style type='text/css'>.htxt{list-style:none;}</style></head><body>"
        HtmlFoot = "</body></html>"
        Conntent=Conntent.replace('&','&#38;')
        Conntent=Conntent.replace(' ','&#160;')
        Conntent=Conntent.replace('<','&#60;')
        Conntent=Conntent.replace('>','&#62;')
        Conntent=Conntent.replace('"','&#34;')
        Conntent=Conntent.replace('\'','&#39;')
        Lines = [HtmlHead]
        for I in Conntent.split('\n'):
            Lines.append("<li class='htxt'>%s</li>" % I)
        Lines.append(HtmlFoot)
        Conntent = '\n'.join(Lines)
        return F._make([True, Conntent, ""])
    except Exception, e:
        return F._make([True, "", str(e)])

