#!/usr/bin/python
# -*- coding: utf-8 -*-

'''跨平台公共库
'''

import xml

from testbase.conf import settings

from adapter.Element import MtControl
from adapter.Element import MtList

if settings.PLATFORM == 'Android':
    from qt4a.andrcontrols import *
    from qt4a.qpath import QPath
    from adapter.Element import ImageView
elif settings.PLATFORM == 'iOS':
    from qt4i.icontrols import *
    from adapter.Element import Element
    from qt4i.qpath import QPath
elif settings.PLATFORM == 'h5':
    from qt4a.andrcontrols import *
    from qt4a.qpath import QPath
    from qt4w.webcontrols import *
elif settings.PLATFORM == 'Cocos Creater':
    from qt4cc.cccontrols import CCScene, CCNode


else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)


def inflate(self, name):
    locator = {}
    dirname = settings.PROJECT_ROOT
    path = os.path.join(os.path.join(os.path.abspath(dirname), "panel"), name)
    dom = xml.dom.minidom.parse(path)
    tree = dom.documentElement
    views = tree.getElementsByTagName("View")

    for view in views:
        dict = {}

        dict["root"] = self

        if view.hasAttribute("name"):
            locator[view.getAttribute("name")] = dict

        if settings.PLATFORM == 'Android':
            android = view.getElementsByTagName("android")[0]
            if android.hasAttribute("type"):
                dict["type"] = globals()[android.getAttribute("type")]
            if android.hasAttribute("locator"):
                dict["locator"] = QPath(android.getAttribute("locator"))
        elif settings.PLATFORM == 'iOS':
            ios = view.getElementsByTagName("ios")[0]
            if ios.hasAttribute("type"):
                dict["type"] = globals()[ios.getAttribute("type")]
            if ios.hasAttribute("locator"):
                dict["locator"] = QPath(ios.getAttribute("locator"))
            if ios.hasAttribute("root"):
                dict["root"] = ios.getAttribute("root")
        elif settings.PLATFORM == 'h5':
            h5 = view.getElementsByTagName("h5")[0]
            if h5.hasAttribute("type"):
                dict["type"] = globals()[h5.getAttribute("type")]
            if h5.hasAttribute("locator"):
                dict["locator"] = XPath(h5.getAttribute("locator"))
        elif settings.PLATFORM == 'Cocos Creator':
            cocos = view.getElementsByTagName("cocos")[0]
            if cocos.hasAttribute("type"):
                dict["type"] = globals()[cocos.getAttribute("type")]
            if cocos.hasAttribute("locator"):
                dict["locator"] = QPath(cocos.getAttribute("locator"))
        else:
            raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)

    metisViews = tree.getElementsByTagName("MetisView")


    for metisView in metisViews:
        dict = {}

        dict["root"] = self
        dict["type"] = MtControl
        if metisView.hasAttribute("instance"):
            dict['instance'] = int(metisView.getAttribute("instance"))

        if metisView.hasAttribute("name"):
            locator[metisView.getAttribute("name")] = dict

    metisLists = tree.getElementsByTagName("MetisList")

    for metisList in metisLists:

        dict = {}
        dict["root"] = self
        dict["type"] = MtList

        if metisList.hasAttribute("name"):
            locator[metisList.getAttribute("name")] = dict

    return locator


if settings.PLATFORM == 'Android':
    pass

elif settings.PLATFORM == 'iOS':
    # TODO: iOS端完善
    pass
elif settings.PLATFORM == 'h5':
    pass
else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)

if __name__ == "__main__":
    print(inflate("test", "LoginPanel.xml"))
