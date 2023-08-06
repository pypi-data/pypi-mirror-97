#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_utils.include module

This module is used for Pyramid integration
"""

import os.path

from chameleon import PageTemplateFile
from persistent import IPersistent
from zope.annotation import IAnnotations, IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations
from zope.keyreference.interfaces import IKeyReference
from zope.keyreference.persistent import KeyReferenceToPersistent

import pyams_utils
from pyams_utils.container import ParentSelector
from pyams_utils.context import ContextSelector
from pyams_utils.i18n import set_locales
from pyams_utils.request import RequestSelector, get_annotations, get_debug, get_display_context
from pyams_utils.tales import ExtensionExpr
from pyams_utils.traversing import NamespaceTraverser


__docformat__ = 'restructuredtext'


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_utils:locales')

    # define locales
    set_locales(config.registry.settings)

    # add request properties
    config.add_request_method(get_annotations, 'annotations', reify=True)
    config.add_request_method(get_debug, 'debug', reify=True)
    config.add_request_method(get_display_context, 'display_context', property=True)

    # define namespace traverser
    config.add_traverser(NamespaceTraverser)

    # add custom subscriber predicates to support events via supported interfaces
    config.add_subscriber_predicate('context_selector', ContextSelector)
    config.add_subscriber_predicate('parent_selector', ParentSelector)
    config.add_subscriber_predicate('request_selector', RequestSelector)

    # load components into registry
    config.registry.registerAdapter(AttributeAnnotations, (IAttributeAnnotatable, ), IAnnotations)
    config.registry.registerAdapter(KeyReferenceToPersistent, (IPersistent, ), IKeyReference)

    config.scan()

    if hasattr(config, 'load_zcml'):
        zcml_name = os.path.join(pyams_utils.__path__[0], 'configure.zcml')
        if os.path.exists(zcml_name):
            config.load_zcml(zcml_name)

    PageTemplateFile.expression_types['tales'] = ExtensionExpr
