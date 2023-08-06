# -*- coding: utf-8 -*-

import math
import time
try:
    import urllib2 as urllib_request
except ImportError:
    import urllib.request as urllib_request

from metislib.controls import MtControl
from metislib.controls import MtList
from testbase import logger
from testbase.conf import settings

from adapter.cache import metis_cache


if settings.PLATFORM == 'iOS':
    from qt4i.icontrols import Element

    class Element(Element):
        def __init__(self, root, locator, **ext):
            super(Element, self).__init__(root, locator, **ext)

        def click(self, offset_x=None, offset_y=None):
            super(Element, self).click(offset_x, offset_y)

        @property
        def text(self):
            return self.value

        @text.setter
        def text(self, text):
            '''设置value(输入，支持中文)
            '''
            self.value = text

        def scroll_to_bottom(self, time=1):
            while time > 0:
                self._app.device.drag(0.5, 0.8, 0.5, 0.5)
                time = time - 1

        def scroll_to_top(self, time=1):
            while time > 0:
                self._app.device.drag(0.5, 0.2, 0.5, 0.5)
                time = time - 1
elif settings.PLATFORM == 'Android':
    from qt4a.andrcontrols import *

    class View(View):
        def __init__(self, activity, root, driver, locator=None, hashcode=0):
            super(View, self).__init__(activity, root, driver, locator, hashcode)

        def wait_for_exist(self, timeout=10, interval=0.5):
            '''等待控件出现
             '''
            time0 = time.time()
            while time.time() - time0 < timeout:
                if self.exist():
                    return True
                time.sleep(interval)
            return False

    class TextView(TextView, View):
        '''包含Text的View 
        '''
        pass

    class EditText(EditText, TextView):
        '''输入文本框
        '''
        pass

    class Button(Button, TextView):
        '''按钮类
        '''
        pass

    class CompoundButton(CompoundButton, Button):
        '''可选按钮，一般用于实现Switch
        '''
        pass

    class RadioButton(RadioButton, CompoundButton):
        '''单选按钮
        '''
        pass

    class CheckBox(CheckBox, CompoundButton):
        '''选择按钮
        '''
        pass

    class CheckedTextView(CheckedTextView, TextView):
        '''可选文本框
        '''
        pass

    class ImageView(ImageView, View):
        '''显示图片控件
        '''
        pass

    class ImageButton(ImageButton, ImageView):
        pass

    class DropdownView(DropdownView, View):
        pass


class MtList(MtList):
    def __init__(self, root, id, region="main", locator=None):
        super(MtList, self).__init__(root, id, region, locator)


class MtControl(MtControl):
    def __init__(self, root, id, locator=None, name=None, instance=None):
        super(MtControl, self).__init__(root, id, locator, name, instance)

    def exist(self):
        '''判断控件是否存在
        '''
        time0 = time.time()
        try:
            flag = super(MtControl, self).exist()
        except urllib_request.HTTPError:
            logger.info("通过metis判断控件 %s 是否存在, 出现HttpError错误" % self.text)
            return False
        cost = time.time() - time0
        logger.info("通过metis判断控件 %s 是否存在耗时 %.2f 秒" % (self.text, cost))
        return flag

    def wait_for_exist(self, timeout=10, interval=0.5):
        '''等待控件出现
         '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.exist():
                return True
            time.sleep(interval)
        return False

    def wait_until_exist(self, timeout=10, interval=0.1):
        '''等待控件,直到出现
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.exist(): return True
            time.sleep(interval)
        raise ControlNotFoundError('控件：%s 未找到' % self.text)

    def _print_uitree(self, driver):
        '''打印窗口的UI树
        '''
        if driver:
            ui_tree = driver.get_uitree()
            lines = []
            for item in ui_tree:
                if item['Id']:
                    _spaces = ''
                    _indent = '|---'
                    _line = _spaces + '{  ' + ',   '.join([
                        'Name: "%s"' % item['Id'],
                        'Type: "%s"' % item['Type'],
                        'Rect: %s' % item['Rect']]) + '  }'
                    lines.append(_line)

    def _get_uitree(self):
        try:
            uitree = {}
            img = self._view.screenshot()
            driver = self._driver_cls(img, self.os_type)
            if driver:
                ui_tree = driver.get_uitree()
                for item in ui_tree:
                    if item['Id']:
                        # uitree[item['Id'].encode('utf-8')] = item['Rect']
                        uitree[item['Id']] = item['Rect']
            return uitree
        except urllib_request.HTTPError:
            logger.info("get_uitree() 出现HttpError错误")
            return False

    def get_uitree(self, timeout=20, interval=0.5):
        '''获取窗口的UI树
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            uitree = self._get_uitree()
            if isinstance(uitree, dict) and len(uitree):
                return uitree
            time.sleep(interval)
        return {}

    def get_uitree_lastname(self):
        '''获取当前UI树中的最后一个控件名
        '''
        lastname = ""
        img = self._view.screenshot()
        driver = self._driver_cls(img, self.os_type)
        if driver:
            ui_tree = driver.get_uitree()
            for item in ui_tree:
                if item['Id']:
                    lastname = item['Id'].encode('utf-8')
        return lastname

    @metis_cache
    def _get_click_location(self, offset_x=None, offset_y=None):
        '''获取控件的点击的位置的坐标
        '''
        # point_x, point_y = super(MtControl, self)._get_click_location(offset_x=offset_x, offset_y=offset_y)
        # return point_x, point_y
        return self.wrap_get_click_location(offset_x, offset_y)

    def wrap_get_click_location(self, offset_x=None, offset_y=None, timeout=20, interval=2):
        '''获取控件的点击的位置的坐标，出现Metis HttpError时重试
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            point = self._wrap_get_click_location(offset_x, offset_y)
            if isinstance(point, tuple):
                return point[0], point[1]
            time.sleep(interval)
        raise RuntimeError("HttpError")

    def _wrap_get_click_location(self, offset_x=None, offset_y=None):
        '''获取控件的点击的位置的坐标，捕捉HttpError
        '''
        try:
            point_x, point_y = super(MtControl, self)._get_click_location(offset_x=offset_x, offset_y=offset_y)
            return point_x, point_y
        except urllib_request.HTTPError:
            logger.info("_get_click_location() 出现HttpError错误")
            return False

    def rect_left(self, rect):
        '''获取控件左侧距离屏幕左边界距离
        '''
        return rect["Left"]

    def rect_right(self, rect):
        '''获取控件右侧距离屏幕右边界距离
        '''
        return rect["Left"] + rect["Width"]

    def rect_bottom(self, rect):
        '''获取控件底部距离屏幕上边界距离
        '''
        return rect["Top"] + rect["Height"]

    def rect_top(self, rect):
        '''获取控件顶部距离屏幕上边界距离
        '''
        return rect["Top"]

    def _get_relative_name(self, direction):
        '''获取控件相对位置的控件名称

        :param direction:       相对位置（left, right, top, bottom）
        :type  direction:       string
        '''
        try:
            x, y, w, h = self.rect
        except urllib_request.HTTPError:
            return False

        left = x
        right = x + w
        top = y
        bottom = y + h
        uitree = self.get_uitree()
        min_value = 10000
        target_name = ""
        if direction == 'right':
            for name, rect in uitree.items():
                # 在右面
                if self.rect_left(rect) > right:
                    if (top < self.rect_top(rect) < bottom) or (top < self.rect_bottom(rect) < bottom):
                        value = self.rect_left(rect) - right
                        if value < min_value:
                            min_value = value
                            target_name = name
            return target_name
        elif direction == 'left':
            for name, rect in uitree.items():
                # 在左面
                if self.rect_right(rect) < left:
                    if (top < self.rect_top(rect) < bottom) or (top < self.rect_bottom(rect) < bottom):
                        value = left - self.rect_right(rect)
                        if value < min_value:
                            min_value = value
                            target_name = name
            return target_name
        elif direction == 'top':
            for name, rect in uitree.items():
                # 在上面
                if self.rect_bottom(rect) < top:
                    if (left < self.rect_left(rect) < right) or (left < self.rect_right(rect) < right):
                        value = top - self.rect_bottom(rect)
                        if value < min_value:
                            min_value = value
                            target_name = name
            return target_name
        elif direction == 'bottom':
            for name, rect in uitree.items():
                # 在下面
                if self.rect_top(rect) > bottom:
                    if (left < self.rect_left(rect) < right) or (left < self.rect_right(rect) < right):
                        value = self.rect_top(rect) - bottom
                        if value < min_value:
                            min_value = value
                            target_name = name
            return target_name
        else:
            raise RuntimeError('不支持的方向：%s' % direction)

    def get_relative_name(self, direction, timeout=20, interval=0.5):
        '''获取控件相对位置的控件名称,出错重试

        :param direction:       相对位置（left, right, top, bottom）
        :type  direction:       string
        '''
        time0 = time.time()
        while time.time() - time0 < timeout:
            name = self._get_relative_name(direction)
            if isinstance(name, str):
                return name
            time.sleep(interval)
        return ""

    def _get_control_pose(self):
        '''获取控件的绝对位置
        '''
        loc_x, loc_y = self._get_click_location()
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self._view._device.screen_size
        pose_x, pose_y = loc_x * screen_width, loc_y * screen_height
        return pose_x, pose_y

    def _get_screen_size(self):
        '''获取屏幕的尺寸
        '''
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self._view._device.screen_size
        # TODO ios screen size
        return screen_width, screen_height

    def click_relative_pose(self, offset_x=0, offset_y=0):
        '''点击当前控件的相对位置,指定偏移量

        :param offset_x:       宽度方向偏移量
        :type  offset_x:       float
        :param offset_y:       高度方向偏移量
        :type  offset_y:       float
        '''
        x, y = self._get_click_location()
        width_ratio, height_ratio = x + offset_x, y + offset_y
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self._view._device.screen_size
            self._view._device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._view._device.click(x=width_ratio, y=height_ratio)

    def click_relative_direction(self, direction, offset=0.1):
        '''点击当前控件的相对位置，指定偏移方向

        :param direction:       控件偏移方向（left, right, top, bottom）
        :type  direction:       string
        :param offset:          在偏移方向上的偏移量
        :type  offset:          float
        '''
        offset_x, offset_y = 0, 0
        if direction == "left":
            offset_x -= offset
        elif direction == "right":
            offset_x += offset
        elif direction == "top":
            offset_y -= offset
        elif direction == "bottom":
            offset_y += offset
        else:
            raise Exception("Unknown direction")
        self.click_relative_pose(offset_x, offset_y)

    def _get_control_near_location(self, x, y):
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
        uitree = self.get_uitree()
        logger.info("length of uitree: %d" % (len(uitree)))
        time0 = time.time()
        while len(uitree) == 0 and time.time() - time0 < 10:
            uitree = self.get_uitree()
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

    def get_control_near_relative_pose(self, offset_x, offset_y):
        '''获取相对当前控件偏移位置最近的控件，包含名称和坐标

        :param offset_x:       宽度方向偏移量
        :type  offset_x:       float
        :param offset_y:       高度方向偏移量
        :type  offset_y:       float
        '''
        x0, y0 = self._get_click_location()
        x, y = x0 + offset_x, y0 + offset_y
        return self._get_control_near_location(x, y)
