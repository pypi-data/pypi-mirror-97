# -*- coding: UTF-8 -*-

from qt4a.andrcontrols import *
from qt4a.qpath import QPath

from adapter.OEDWindow import OEDWindow


class QQChatPanel(OEDWindow):
    Activity = 'com.tencent.mobileqq.activity.SplashActivity'  # QQ首页界面

    def __init__(self, app, leave_time=2):
        super(QQChatPanel, self).__init__(app, leave_time=leave_time)
        self.update_locator({
            '首页': {'type': TextView, 'root': self,
                   'locator': QPath(
                       '/Text="ke.qq.com" && Visible="True" && Instance="1"')},
            '首个会话': {'type': RelativeLayout, 'root': self, 'locator': QPath('/Id="relativeItem" && Instance="1"')},
            '输入': {'type': EditText, 'root': self, 'locator': QPath('/Id="input"')},
            '发送': {'type': Button, 'root': self, 'locator': QPath('/Text="发送" && Instance="0"')}
        })

    def goto_homepage(self, url):
        self.Controls["首个会话"].click()
        time.sleep(2)
        if self.Controls["首页"].exist():
            self.Controls["首页"].click()
            time.sleep(3)
        else:
            self.Controls["输入"].send_text(url)
            self.Controls["发送"].click()
            self.Controls["首页"].click()
            time.sleep(3)
