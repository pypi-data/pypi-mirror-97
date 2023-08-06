#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_utils.timezone.utility module

"""

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_utils.interfaces.timezone import IServerTimezone


__docformat__ = 'restructuredtext'


@implementer(IServerTimezone)
class ServerTimezoneUtility(Persistent, Contained):
    """Server timezone utility"""

    timezone = FieldProperty(IServerTimezone['timezone'])
