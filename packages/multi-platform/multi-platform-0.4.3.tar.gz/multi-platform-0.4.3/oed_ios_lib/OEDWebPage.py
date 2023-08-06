# -*- coding: utf-8 -*-

from qt4w.webcontrols import *
from qt4i.web import IOSWebView
from qt4i.icontrols import *

'''
Ke WebPage类
'''


class OEDWebPage(WebPage):
    def __init__(self, webview_or_webpage):
        super(OEDWebPage, self).__init__(IOSWebView(webview_or_webpage, QPath('/classname="WebView" & maxdepth=12')))
