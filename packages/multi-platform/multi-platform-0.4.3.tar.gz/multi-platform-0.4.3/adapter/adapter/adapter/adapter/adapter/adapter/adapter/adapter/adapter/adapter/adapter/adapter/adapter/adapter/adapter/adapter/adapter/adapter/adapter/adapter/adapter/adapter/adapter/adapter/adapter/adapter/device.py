# -*- coding: UTF-8 -*-

'''跨平台Device类
'''


class Device(object):
    '''
    '''

    def __init__(self, device):
        self._device = device

    def get_device(self):
        return self._device
