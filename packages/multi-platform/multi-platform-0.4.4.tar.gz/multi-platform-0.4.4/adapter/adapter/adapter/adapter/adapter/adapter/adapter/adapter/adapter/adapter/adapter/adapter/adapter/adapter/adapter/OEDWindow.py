# -*- coding: UTF-8 -*-

import time
from oed_native_lib.OEDWindow import OEDWindow
from adapter.Element import MtControl
from testbase.conf import settings
from testbase import logger
from testbase import TestCase
from testbase.util import ThreadGroupLocal
import testbase
import math
from enum import Enum
from tuia.exceptions import ControlAmbiguousError


class OEDXWindow(OEDWindow):
    '''跨平台 Window类
    '''
    class Option(Enum):
        '''操作判断选项
        '''
        DEFAULT = ""
        APPEAR = "appear"
        DISAPPEAR = "disappear"

    def __init__(self, OEDApp, **kwds):
        OEDWindow.__init__(self, OEDApp, **kwds)

    def updateLocator(self, locators):
        if settings.PLATFORM == "Android" or settings.PLATFORM == "h5":
            super(OEDXWindow, self).update_locator(locators)
        else:
            super(OEDXWindow, self).updateLocator(locators)

    def wait_for_exist(self, timeout=10, interval=0.5):
        '''等待页面出现
        '''
        if settings.PLATFORM == "h5":
            self.Activity = "com.tencent.mobileqq.activity.QQBrowserActivity"
        try:
            return super(OEDXWindow, self).wait_for_exist(timeout, interval)
        except Exception as e:
            return False

    def click_screen(self, width_ratio=0.5, height_ratio=0.5):
        '''点击屏幕

        :param width_ratio:    宽度方向百分比
        :type  width_ratio:    float
        :param height_ratio:   宽度方向百分比
        :type  height_ratio:   float
        '''
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)

    def _get_screen_size(self):
        '''获取屏幕尺寸
        '''
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size
            return screen_width, screen_height
        if settings.PLATFORM == "iOS":
            return  # TODO

    def double_click_screen(self, width_ratio=0.5, height_ratio=0.5):
        '''双击屏幕

        :param width_ratio:    宽度方向百分比
        :type  width_ratio:    float
        :param height_ratio:   宽度方向百分比
        :type  height_ratio:   float
        '''
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)
            self._device.click(x=width_ratio, y=height_ratio)

    def _click_defined_control(self, control, timeout=30, interval=1):
        '''点击指定控件

        :param control:    控件名称
        :type  control:    string
        :param timeout:    超时时间
        :type  timeout:    float
        :param interval:   重试等待时间
        :type  interval:   float
        '''
        time0 = time.time()
        self.add_control(control)
        while time.time() - time0 < timeout:
            if self.Controls[control].wait_for_exist():
                logger.info("点击 %s" % control)
                self.Controls[control].click()
                return True
            time.sleep(interval)
        logger.info("%s 不存在" % control)

    def click_control(
            self, control, option="", judge_control="",
            timeout=30, interval=1):
        '''点击指定控件，直到原控件消失/新控件出现

        :param control:           控件名称
        :type  control:           string
        :param timeout:           超时时间(常在控件建议30s，常无控件建议5s)
        :type  timeout:           float
        :param interval:          重试等待时间
        :type  interval:          float
        :param option:            确认点击成功的条件（disappear:控件消失, appear:控件出现）
        :type  option:            string
        :param judge_control:     判定控件名称
        :type  judge_control:     string
        '''
        time0 = time.time()
        self.add_control(control)
        if self.Controls[control].wait_for_exist():
            logger.info("点击 %s" % control)
            self.Controls[control].click()
            time.sleep(interval)
        if not option:
            return
        # assert option in self.Option.__members__, "Unknown option"
        if judge_control:
            self.add_control(judge_control)
        else:
            judge_control = control
        while time.time() - time0 < timeout:
            if option == "disappear":
                if self.Controls[control].wait_for_exist():
                    time.sleep(interval)
                    if self.Controls[judge_control].wait_for_exist():
                        logger.info("再次点击 %s" % judge_control)
                        self.Controls[control].click()
                    else:
                        continue
                else:
                    logger.info("%s 已消失" % judge_control)
                    return True
            elif option == "appear":
                assert judge_control != "", "judge_control 不能为空"
                if not self.Controls[judge_control].wait_for_exist():
                    time.sleep(interval)
                    if not self.Controls[judge_control].wait_for_exist():
                        logger.info("再次点击 %s" % judge_control)
                        self.Controls[control].click()
                    else:
                        continue
                else:
                    logger.info("%s 已出现" % control)
                    return True
            else:
                return True
        logger.info("点击 %s 超时" % control)

    def click_location(
            self, x, y, option="", judge_control="",
            timeout=30, interval=1):
        '''点击指定位置，直到控件消失/出现

        :param x, y:              点击位置
        :type  control:           string
        :param timeout:           超时时间(常在控件建议30s，常无控件建议5s)
        :type  timeout:           float
        :param interval:          重试等待时间
        :type  interval:          float
        :param option:            确认点击成功的条件（disappear:控件消失, appear:控件出现）
        :type  option:            string
        :param judge_control:     判定控件名称
        :type  judge_control:     string
        '''
        time0 = time.time()
        self.click_screen(x, y)
        time.sleep(interval)
        if not option:
            return
        assert judge_control != "", "judge_control 不能为空"
        control = judge_control
        self.add_control(control)
        while time.time() - time0 < timeout:
            if option == "disappear":
                if self.Controls[control].wait_for_exist():
                    time.sleep(interval)
                    if self.Controls[judge_control].wait_for_exist():
                        logger.info("再次点击")
                        self.click_screen(x, y)
                    else:
                        continue
                else:
                    logger.info("%s 已消失" % judge_control)
                    return True
            elif option == "appear":
                if not self.Controls[judge_control].wait_for_exist():
                    time.sleep(interval)
                    if not self.Controls[judge_control].wait_for_exist():
                        logger.info("再次点击")
                        self.click_screen(x, y)
                    else:
                        continue
                else:
                    logger.info("%s 已出现" % control)
                    return True
            else:
                return True
        logger.info("点击超时")

    def touch_skip(self):
        '''点击跳过
        '''
        control = "跳过"
        self._click_defined_control(control, timeout=20)

    def touch_skip_select(self, timeout=5, interval=0.5):
        '''跳过选择学院

        : param timeout:    超时时间
        : type  timeout:    float
        : param interval:   重试等待时间
        : type  interval:   float
        '''
        control = "跳过选择学院"
        self._click_defined_control(control, timeout, interval)

    def click_confirm(self, timeout=5, interval=0.5):
        '''点击确认
        '''
        control = "确认"
        self._click_defined_control(control)

    def click_ensure(self, timeout=5, interval=0.5):
        '''点击确定
        '''
        control = "确定"
        self._click_defined_control(control)

    def click_cancel(self):
        '''点击取消
        '''
        control = "取消"
        self._click_defined_control(control)

    def click_defined_element(self, control, search_page=5):
        '''点击指定控件，支持翻页查找

        : param control:       控件名
        : type  control:       string
        : param search_page:   查找最大页数
        : type  search_page:   int
        '''
        self.add_control(control)
        self.wait_for_exist(timeout=5, interval=2)
        self.Controls[control].wait_for_exist(timeout=5, interval=0.5)
        for i in range(search_page):
            if self.Controls[control].wait_for_exist():
                self.Controls[control].click()
                return True
            if i < search_page - 1:
                self.swipe_pagedown()
        raise Exception("未找到元素 %s" % control)

    def verify_element_existence(self, control, search_page=1):
        '''确认控件是否存在，支持翻页查找

        : param control:       控件名
        : type  control:       string
        : param search_page:   查找最大页数
        : type  search_page:   int
        '''
        self.add_control(control)
        self.wait_for_exist(timeout=5, interval=2)
        for i in range(search_page):
            if self.Controls[control].wait_for_exist():
                logger.info("%s 存在" % control)
                return True
            if i < search_page - 1:
                self.swipe_pagedown()
        logger.info(
            "%s 不存在! Controls: %s" % (control, self.get_all_control_names()))
        return False

    def show_uitree(self):
        '''打印当前页面的UI树，本地测试用
        '''
        self.add_control("Mt")
        ui_tree = self.Controls['Mt'].get_uitree()
        for id, rect in ui_tree.items():
            if id:
                print('Id: "%s" | Rect: "%s"' % (id, rect))

    def add_control(self, control, type=MtControl, instance=0):
        '''增加临时控件，无需在xml中预先添加

        : param control:       控件名
        : type  control:       string
        : param type:          控件类型
        : type  type:          class_name
        : param instance:      控件序号
        : type  instance:      int
        '''
        if control not in self._locators.keys():
            self.updateLocator(
                {control: {'type': type, 'root': self, 'instance': instance}})

    def click_first_of_repeat_control(self, control):
        '''点击重复控件的第一个 （待删，请勿使用）

        : param control:       控件名
        : type  control:       string
        '''
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            logger.info("重复控件，点击第一个")
            self.updateLocator(
                {control + "-0": {
                    'type': MtControl,
                    'root': self,
                    'name': control,
                    'instance': 0}})
            self.click_defined_element(control + "-0")

    def click_last_of_repeat_control(self, control):
        '''点击重复控件的最后一个 （待删，请勿使用）

        : param control:       控件名
        : type  control:       string
        '''
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            logger.info("重复控件，点击最后一个")
            control_names = self.get_all_control_names()
            logger.info("control_names: %s" % control_names)
            count = control_names.count(control)
            instance_num = "-%d" % (count - 1)
            self.updateLocator(
                {control + instance_num: {
                    'type': MtControl,
                    'root': self,
                    'name': control,
                    'instance': count - 1}})
            self.click_defined_element(control + instance_num)

    def click_any_of_repeat_control(self, control, instance=0):
        '''点击重复控件的任意一个, instance为index

        : param control:       控件名
        : type  control:       string
        : param instance:      控件索引
        : type  instance:      int
        '''
        suffix = "-%d" % instance
        logger.info("点击 %s" % (control + suffix))
        self.updateLocator(
            {control + suffix: {
                'type': MtControl,
                'root': self,
                'name': control,
                'instance': instance}})
        self.click_defined_element(control + suffix)

    def swipe_pagedown(self):
        '''翻到下一页
        '''
        logger.info("翻到下一页")
        self._app.swipe_pagedown()

    def swipe_pageup(self):
        '''翻到上一页
        '''
        logger.info("翻到上一页")
        self._app.swipe_pageup()

    def swipe_to_visible(self, control, page=5):
        '''向下翻页，直到控件可见

        : param control:       控件名
        : type  control:       string
        : param page:   翻页最大页数
        : type  page:   int
        '''
        self.add_control(control)
        for _ in range(page):
            if self.Controls[control].wait_for_exist():
                logger.info("Find %s" % control)
                return
            else:
                self.swipe_pagedown()
        logger.info("Not find %s in %s pages" % (control, page))

    def swipe_screen_oriented(self, x, y, direction, count=1):
        '''沿固定方向滑动屏幕

        : param x， y:       滑动点起点位置（屏幕百分比 0-1）
        : type x， y:        float
        : param direction:   滑动方向 (left, right, top, bottom)
        : type direction:    string
        : param count:       次数
        : type count:        int
        '''
        logger.info("向%s方向滑动" % direction)
        self._app.swipe_screen_oriented(x, y, direction, count=1)

    def swipe_screen(self, x1, y1, x2, y2, count=1):
        '''沿固定方向滑动屏幕

        : param x1， y1:       滑动点起点位置（屏幕百分比 0-1）
        : type x1， y1:        float
        : param x2， y2:       滑动点终点位置（屏幕百分比 0-1）
        : type x2， y2:        float
        : param count:         次数
        : type count:          int
        '''
        self._app.swipe_screen(x1, y1, x2, y2, count)

    def get_all_control_names(self):
        '''获取所有控件名称
        '''
        self.add_control("controls")
        uitree = self.Controls['controls'].get_uitree()
        control_names = ' | '.join(uitree.keys())
        return control_names

    def get_control_names_in_window(self, x0=0, y0=0, x1=1, y1=1):
        '''获取坐标范围内的控件

        : param x0， y0:       滑动点起点位置（屏幕百分比 0-1）
        : type x0， y0:        float
        : param x1， y1:       滑动点终点位置（屏幕百分比 0-1）
        : type x1， y1:        float
        '''
        self.add_control("controls")
        width, height = self.device.screen_size
        px0, py0 = x0 * width, y0 * height
        px1, py1 = x1 * width, y1 * height
        control_names = []
        uitree = self.Controls['controls'].get_uitree()
        for name, rect in uitree.items():
            if px0 < rect['Left'] + 0.5 * rect['Width'] < px1 and \
                    py0 < rect['Top'] + 0.5 * rect['Height'] < py1:
                control_names.append(name)
        return control_names

    def get_control_name_by_partial(self, partial, option="in"):
        '''通过部分控件名查找完整控件名

        : param partial:       部分控件名
        : type partial:        string
        : param option:        查找选项（in , startswith, endswith）
        : type option:         string
        '''
        self.add_control('controls')
        uitree = self.Controls['controls'].get_uitree()
        for name in uitree.keys():
            if option == 'startswith':
                if name.startswith(partial):
                    return name
            elif option == 'endswith':
                if name.endswith(partial):
                    return name
            else:
                if partial in name:
                    return name
        logger.info("当前页面没有包含 %s 的控件" % partial)
        logger.info("All controls: %s" % (self.get_all_control_names()))

    def take_screen_shot(self, info="获取当前页面截图"):
        '''获取当前页面截图
        '''
        testcase = ThreadGroupLocal().testcase
        testcase.take_screen_shot(self._app, info)

    def get_control_near_location(self, x, y):
        '''获取距离指定坐标最近的控件,包含控件名称和坐标

        :param x:       宽度方向坐标
        :type  x:       float
        :param y:       高度方向坐标
        :type  y:       float
        '''
        width, height = self._get_screen_size()
        px0, py0 = x * width, y * height
        min_distance = float("inf")
        control = dict()
        name = None
        self.add_control("controls")
        uitree = self.Controls['controls'].get_uitree()
        logger.info("length of uitree: %d" % (len(uitree)))
        time0 = time.time()
        while len(uitree) == 0 and time.time() - time0 < 10:
            uitree = self.Controls['controls'].get_uitree()
            logger.info("length of uitree: %d" % (len(uitree)))
        for name, rect in uitree.items():
            if rect['Left'] < px0 < rect['Left'] + rect['Width'] and \
                    rect['Top'] < py0 < rect['Top'] + rect['Height']:
                logger.info("Find within control: %s" % name)
                px = rect['Left'] + 0.5 * rect['Width']
                py = rect['Top'] + 0.5 * rect['Height']
                x, y = px / width, py / height
                control = {'name': name, 'location': {'x': x, 'y': y}}
                return control
            else:
                px1 = rect['Left'] + 0.5 * rect['Width']
                py1 = rect['Top'] + 0.5 * rect['Height']
                d = math.sqrt(pow(px1 - px0, 2) + pow(py1 - py0, 2))
                if d < min_distance:
                    min_distance = d
                    x, y = px1 / width, py1 / height
                    control = {'name': name, 'location': {'x': x, 'y': y}}
        if not name:
            logger.error("Find nothing in current page")
            raise Exception("No valid control find")
        logger.info("Find nearest control: %s" % control['name'])
        return control

    def send_back_key(self):
        '''发送返回按键事件
        '''
        self._app.send_back_key()

    def input_text(self, text):
        '''在输入框中输入文本内容
        
        :param text:       输入的文本内容
        :type  text:       str
        '''
        self._app.input_text(text)

    @classmethod
    def ensure_operation(cls, control='default', option='default',
                         timeout=30, interval=1):
        '''点击指定控件，直到原控件消失/新控件出现

        :param control:           控件名称
        :type  control:           string
        :param option:            确认点击成功的条件（disappear:控件消失, appear:控件出现）
        :type  option:            string
        :param timeout:           超时时间(常在控件建议30s，常无控件建议5s)
        :type  timeout:           float
        :param interval:          重试等待时间
        :type  interval:          float
        :param judge_control:     判定控件名称
        :type  judge_control:     string
        '''
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                options = Enum('option', ('appear', 'disappear', 'default'))
                if option not in options.__members__:
                    logger.error("unknown option")
                func(self, *args, **kwargs)
                time.sleep(interval)
                if control:
                    self.add_control(control)
                time0 = time.time()
                while time.time() - time0 < timeout:
                    if option == "disappear":
                        if self.Controls[control].wait_for_exist():
                            time.sleep(interval)
                            if self.Controls[control].wait_for_exist():
                                logger.info("再次尝试 %s" % func.__name__)
                                func(self, *args, **kwargs)
                            else:
                                continue
                        else:
                            logger.info("%s 已消失" % control)
                            return True
                    elif option == "appear":
                        if not self.Controls[control].wait_for_exist():
                            time.sleep(interval)
                            if not self.Controls[control].wait_for_exist():
                                logger.info("再次尝试 %s" % func.__name__)
                                func(self, *args, **kwargs)
                            else:
                                continue
                        else:
                            logger.info("%s 已出现" % control)
                            return True
                    elif option == 'default':
                        return True
                logger.info("超时未成功")
            return wrapper
        return decorator
