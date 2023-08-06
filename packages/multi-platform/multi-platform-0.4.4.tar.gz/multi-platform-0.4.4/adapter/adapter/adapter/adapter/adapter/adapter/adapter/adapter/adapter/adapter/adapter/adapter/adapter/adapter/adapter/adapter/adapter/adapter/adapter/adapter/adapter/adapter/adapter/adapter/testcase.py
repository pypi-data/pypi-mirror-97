# -*- coding: utf-8 -*-
'''示例测试用例
'''
# 2018/05/16 QTAF自动生成

from testbase.conf import settings

from adapter.device import Device

TESTBASE_CLS = None
if settings.PLATFORM == 'Android':
    from qt4a.androidtestbase import AndroidTestBase

    TESTBASE_CLS = AndroidTestBase

elif settings.PLATFORM == 'iOS':
    from qt4i.itestcase import iTestCase

    TESTBASE_CLS = iTestCase

elif settings.PLATFORM == 'h5':
    from qt4a.androidtestbase import AndroidTestBase

    TESTBASE_CLS = AndroidTestBase
else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)


class OEDXTestCase(TESTBASE_CLS):
    '''KeX测试用例基类
    '''
    cache = True

    def init_test(self, testresult):
        '''测试用例初始化
        '''
        super(OEDXTestCase, self).init_test(testresult)

    def start_step(self, step):
        '''支持精准测试
        '''
        super(OEDXTestCase, self).start_step(step)

    def acquire_device(self, *args, **kwargs):
        '''申请设备
        '''
        if settings.PLATFORM == 'Android':
            device = super(OEDXTestCase, self).acquire_device(*args, **kwargs)
            device.adb.start_logcat()
            return Device(device)
        elif settings.PLATFORM == 'iOS':
            from qt4i.device import Device as IosDevice
            idev = IosDevice(*args, **kwargs)
            return Device(idev)
        elif settings.PLATFORM == 'h5':
            device = super(OEDXTestCase, self).acquire_device(*args, **kwargs)
            device.adb.start_logcat()
            return Device(device)

    def post_test(self):
        super(OEDXTestCase, self).post_test()
