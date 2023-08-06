# -*- coding: utf-8 -*-
# @Time     ： 2020/11/24 10:32 上午
# @Author   :  haleli
import hashlib
import os
import pickle
import time

from testbase import logger
from testbase.conf import settings
from testbase.util import ThreadGroupLocal

dirname = settings.PROJECT_ROOT
cache_root_dir = os.path.join(os.path.abspath(dirname), "cache")

if not os.path.exists(cache_root_dir):
    os.makedirs(cache_root_dir)


def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def cache_key(f, *args, **kwargs):
    s = '%s-%s-%s' % (f.__name__, str(args), str(kwargs))
    return os.path.join(cache_root_dir, '%s.dump' % md5(s))


def metis_cache_key(root, text, platform, device_id, *args, **kwargs):
    s = '%s-%s-%s-%s-%s-%s' % (type(root).__name__, text, platform, device_id, str(args), str(kwargs))
    return os.path.join(cache_root_dir, '%s.dump' % md5(s))


def cache(f):
    def wrap(*args, **kwargs):
        fn = cache_key(f, *args, **kwargs)
        if os.path.exists(fn):
            logger.info('loading cache')
            with open(fn, 'rb') as fr:
                return pickle.load(fr)

        obj = f(*args, **kwargs)
        with open(fn, 'wb') as fw:
            pickle.dump(obj, fw)
        return obj

    return wrap


def metis_cache(f):
    def wrap(self, *args, **kwargs):
        cache = ThreadGroupLocal().testcase.cache
        if cache:
            text = self.text
            if settings.PLATFORM == "iOS":
                view_or_window = self._view.element
                platform = 'ios'
                device_id = self._view.element._device.udid
            else:
                view_or_window = self._view._view_or_window
                platform = 'android'
                device_id = self._view._device.device_id

            fn = metis_cache_key(view_or_window, text, platform, device_id, *args, **kwargs)
            if os.path.exists(fn):
                logger.info('loading cache')
                time0 = time.time()
                with open(fn, 'rb') as fr:
                    obj = pickle.load(fr)
                    cost = time.time() - time0
                    logger.info("使用缓存查找控件 %s 耗时 %.2f 秒" % (self.text, cost))
                    return obj
        time0 = time.time()
        obj = f(self, *args, **kwargs)
        cost = time.time() - time0
        logger.info("使用metis查找控件 %s 耗时 %.2f 秒" % (self.text, cost))
        if cache:
            with open(fn, 'wb') as fw:
                pickle.dump(obj, fw)
        return obj

    return wrap
