# -*- coding: UTF-8 -*-

'''Ke App类
'''

import time

from qt4a.androidapp import AndroidApp


class OEDApp(AndroidApp):
    '''
    '''
    package_name = 'com.tencent.mobileqq'
    start_activity = 'com.tencent.mobileqq.activity.SplashActivity'

    def __init__(self, device, kill_process=True, start_activity=True, clear_data=True, choose_user_guide=False):
        super(OEDApp, self).__init__(self.__class__.package_name, device)
        self.re_install = True
        self.choose_user_guide = choose_user_guide

        if kill_process:
            self._device.kill_process(self.__class__.package_name)

        if clear_data:
            self._device.clear_data(self.__class__.package_name)
        else:
            self.re_install = False

        if start_activity:
            self.start()

    def start(self):
        '''启动应用
        '''
        self._device.start_activity(self.__class__.package_name + '/' + self.__class__.start_activity)

        time.sleep(7)
