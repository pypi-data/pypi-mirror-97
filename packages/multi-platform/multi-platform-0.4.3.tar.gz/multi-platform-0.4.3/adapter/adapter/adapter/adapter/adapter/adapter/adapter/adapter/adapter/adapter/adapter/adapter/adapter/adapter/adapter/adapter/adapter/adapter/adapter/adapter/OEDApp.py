# -*- coding: UTF-8 -*-

'''跨平台Ke App类
'''

# import time
from oed_native_lib.OEDApp import OEDApp


class OEDXApp(OEDApp):
    '''跨平台App类
    '''

    def __init__(self, device, *args, **kwargs):
        self._device = device
        super(OEDXApp, self).__init__(device._device)
