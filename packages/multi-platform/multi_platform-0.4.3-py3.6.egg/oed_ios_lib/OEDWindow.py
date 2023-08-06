# -*- coding: utf-8 -*-
from qt4i.icontrols import *


class OEDWindow(Window):
    def __init__(self, app, **kwds):
        super(OEDWindow, self).__init__(app)
        self._device = app._device
