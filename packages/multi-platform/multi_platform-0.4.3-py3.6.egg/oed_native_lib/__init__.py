# -*- coding: UTF-8 -*-

'''Ke Native层库
'''

import sys

from testbase.conf import settings

if settings.PLATFORM == 'Android':
    del sys.modules['oed_native_lib']
    import sys
    import oed_android_lib

    sys.modules['oed_native_lib'] = oed_android_lib
elif settings.PLATFORM == 'iOS':
    del sys.modules['oed_native_lib']
    import sys
    import oed_ios_lib

    sys.modules['oed_native_lib'] = oed_ios_lib

elif settings.PLATFORM == 'h5':
    del sys.modules['oed_native_lib']
    import sys
    import oed_h5_lib

    sys.modules['oed_native_lib'] = oed_h5_lib
else:
    raise NotImplementedError('Not supported platform %s' % settings.PLATFORM)
