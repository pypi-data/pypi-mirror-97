# -*- coding: UTF-8 -*-
'''
Ke Window类
'''
from qt4a.andrcontrols import *


class OEDWindow(Window):
    def __init__(self, app, **kwds):
        super(OEDWindow, self).__init__(app, wait_activity=True, **kwds)
