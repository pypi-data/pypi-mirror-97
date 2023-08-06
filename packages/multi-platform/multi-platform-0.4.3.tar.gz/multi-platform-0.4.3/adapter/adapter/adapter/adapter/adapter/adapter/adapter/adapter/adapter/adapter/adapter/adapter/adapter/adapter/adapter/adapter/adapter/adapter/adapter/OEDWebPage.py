# -*- coding: UTF-8 -*-

from oed_native_lib.OEDWebPage import OEDWebPage


class OEDXWebPage(OEDWebPage):
    '''
    跨平台Ke WebPage类
    '''

    def __init__(self, webview_or_webpage):
        super(OEDXWebPage, self).__init__(webview_or_webpage)
