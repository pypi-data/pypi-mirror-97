# -*- coding: UTF-8 -*-

'''Ke App类
'''

import time
from qt4a.androidapp import AndroidApp
from testbase.conf import settings


class OEDApp(AndroidApp):
    '''
    OEDApp for Android基类
    '''
    package_name = settings.PACKAGE_NAME
    start_activity = settings.START_ACTIVITY

    def __init__(self, device, kill_process=True, start_activity=True, clear_data=True, choose_user_guide=False):
        super(OEDApp, self).__init__(self.__class__.package_name, device)

        if settings.DEBUG:
            kill_process = False
            start_activity = False
            clear_data = False

        self.re_install = True
        self.choose_user_guide = choose_user_guide

        # 辅导的debug包也进行了控件Id混淆
        if hasattr(settings, 'QT4A_USE_INT_VIEW_ID') and settings.QT4A_USE_INT_VIEW_ID:
            self._use_int_view_id = True
        else:
            pass

        if kill_process:
            self._device.kill_process(self.__class__.package_name)

        if clear_data:
            self._device.clear_data(self.__class__.package_name)
        else:
            self.re_install = False

        self.grant_all_runtime_permissions()
        self.enable_system_alert_window()

        if start_activity:
            self.start()

    def start(self):
        '''启动应用
        '''
        self._device.start_activity(self.__class__.package_name + '/' + self.__class__.start_activity)
        time.sleep(3)

    def swipe_screen(self, x1, y1, x2, y2, count=1):
        '''自由滑动屏幕
        :param x1， y1: 滑动点起点位置（屏幕百分比 0-1）
        :param x2, y2: 滑动点终点位置（屏幕百分比 0-1）
        :param count:     次数
        '''
        width, height = self.device.screen_size
        x1, y1 = width * x1, height * y1
        x2, y2 = width * x2, height * y2
        for _ in range(count):
            self.get_driver().drag(x1, y1, x2, y2)
            time.sleep(0.5)

    def swipe_screen_oriented(self, x, y, direction, count=1):
        '''沿固定方向滑动屏幕
        :param x， y: 滑动点起点位置（屏幕百分比 0-1）
        :param direction: 滑动方向 (left, right, top, bottom)
        :param count:     次数
        '''
        width, height = self.device.screen_size
        x1, y1 = width * x, height * y
        x2, y2 = x1, y1
        if direction == 'right':
            x2 += width
        elif direction == 'left':
            x2 -= width
        elif direction == 'top':
            y2 -= height
        elif direction == 'bottom':
            y2 += height
        else:
            raise RuntimeError('不支持的方向：%s' % direction)
        for _ in range(count):
            self.get_driver().drag(x1, y1, x2, y2)
            time.sleep(0.5)

    def swipe_pagedown(self, count=1):
        '''滑动屏幕至下一页
        :param count:     次数
        :type  count:     int
        '''
        width, height = self.device.screen_size
        x1, y1 = width // 2, height // 2
        x2, y2 = x1, y1
        y2 = y1 - int(height)
        for _ in range(count):
            self.get_driver().drag(x1, y1, x2, y2)
            time.sleep(1)

    def write_text(self, text):
        self.device.send_text(text)

    def swipe_pageup(self, count=1):
        '''滑动屏幕至下一页
        :param count:     次数
        :type  count:     int
        '''
        width, height = self.device.screen_size
        x1, y1 = width // 2, height // 2
        x2, y2 = x1, y1
        y2 = y1 + int(height)
        for _ in range(count):
            self.get_driver().drag(x1, y1, x2, y2)
            time.sleep(0.5)

    def send_back_key(self):
        '''发送返回按键事件
        '''
        self.device.run_shell_cmd('input keyevent 4')

    def input_text(self, text):
        '''在输入框中输入文本内容
        
        :param text:       输入的文本内容
        :type  text:       str
        '''
        self.device.run_shell_cmd('input text "%s"' % text)
