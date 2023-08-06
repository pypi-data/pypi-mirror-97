# -*- coding: UTF-8 -*-

import time

from qt4a.andrcontrols import *
from qt4a.qpath import QPath

from adapter.OEDWindow import OEDWindow


class QQLoginPanel(OEDWindow):
    Activity = 'com.tencent.mobileqq.activity.LoginActivity'

    def __init__(self, app, leave_time=2):
        super(QQLoginPanel, self).__init__(app, leave_time=leave_time)
        self.update_locator({
            '登录': {'type': Button, 'root': self, 'locator': QPath('/Id="btn_login"')},
            '帐号': {'type': EditText, 'root': self, 'locator': QPath('/Type="bcck" && Id="0x20e"')},
            '密码': {'type': EditText, 'root': self, 'locator': QPath('/Id="password"')},
            '提交': {'type': TextView, 'root': self, 'locator': QPath('/Id="login"')},
            '同意': {'type': TextView, 'root': self, 'locator': QPath('/Text="同意"')},
        })

    def login(self, acc, pwd):
        print("帐号 %s" % acc)
        print("密码 %s" % pwd)
        acc = "384847349"
        pwd = "1qa2ws3ed"
        if self.wait_for_exist(timeout=5, interval=0.5):
            if self.Controls["同意"].exist():
                self.Controls["同意"].click()
                time.sleep(2)
            if (self.Controls["登录"].exist()):
                self.Controls["登录"].click()
            time.sleep(3)
            self.Controls["帐号"].send_text(acc)
            self.Controls["密码"].send_text(pwd)
            time.sleep(1)

            if (self.Controls["提交"].exist()):
                self.Controls["提交"].click()
