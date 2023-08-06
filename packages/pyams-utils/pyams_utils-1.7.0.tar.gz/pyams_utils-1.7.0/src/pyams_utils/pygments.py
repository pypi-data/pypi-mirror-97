#
# Copyright (c) 2008-2018 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_utils.pygments module

This module is used to provide an URL which allows you to load Pygments CSS files.
It also provides two vocabularies of available lexers and styles.
"""

from fanstatic import get_library_registry
from persistent import Persistent
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer
from pygments.styles import get_all_styles
from pyramid.response import Response
from pyramid.view import view_config
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_utils.factory import factory_config
from pyams_utils.fanstatic import ExternalResource
from pyams_utils.interfaces.pygments import IPygmentsCodeConfiguration, \
    PYGMENTS_LEXERS_VOCABULARY_NAME, PYGMENTS_STYLES_VOCABULARY_NAME
from pyams_utils.list import unique_iter
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'

from pyams_utils import _


#
# Pygments CSS view
#

for library in get_library_registry().values():
    break
else:
    try:
        from pyams_skin import library
    except ImportError:
        try:
            from pyams_default_theme import library
        except ImportError:
            library = None


# pylint: disable=invalid-name
if library is not None:
    pygments_css = ExternalResource(library, 'get-pygments-style.css', resource_type='css')
else:
    pygments_css = None


@view_config(name='get-pygments-style.css')
def get_pygments_style_view(request):
    """View used to download Pygments style"""
    style = request.params.get('style', 'default')
    styles = HtmlFormatter(linenos='inline',
                           nowrap=False,
                           cssclass='source',
                           style=style).get_style_defs()
    return Response(styles, content_type='text/css')


#
# Pygments lexers
#

@vocabulary_config(name=PYGMENTS_LEXERS_VOCABULARY_NAME)
class PygmentsLexersVocabulary(SimpleVocabulary):
    """Pygments lexers vocabulary"""

    def __init__(self, context):  # pylint: disable=unused-argument
        terms = [SimpleTerm('auto', title=_("Automatic detection"))]
        # pylint: disable=unused-variable
        for name, aliases, filetypes, mimetypes in sorted(unique_iter(get_all_lexers(),
                                                                      key=lambda x: x[0].lower()),
                                                          key=lambda x: x[0].lower()):
            terms.append(SimpleTerm(aliases[0] if len(aliases) > 0 else name,
                                    title='{0}{1}'.format(name,
                                                          ' ({})'.format(', '.join(filetypes))
                                                          if filetypes else '')))
        super().__init__(terms)


@vocabulary_config(name=PYGMENTS_STYLES_VOCABULARY_NAME)
class PygmentsStylesVocabulary(SimpleVocabulary):
    """Pygments styles vocabulary"""

    def __init__(self, context):  # pylint: disable=unused-argument
        terms = []
        for name in sorted(get_all_styles()):
            terms.append(SimpleTerm(name))
        super().__init__(terms)


#
# Pygments configuration
#

@factory_config(IPygmentsCodeConfiguration)
class PygmentsCodeRendererSettings(Persistent, Contained):
    """Pygments code renderer settings"""

    lexer = FieldProperty(IPygmentsCodeConfiguration['lexer'])
    display_linenos = FieldProperty(IPygmentsCodeConfiguration['display_linenos'])
    disable_wrap = FieldProperty(IPygmentsCodeConfiguration['disable_wrap'])
    style = FieldProperty(IPygmentsCodeConfiguration['style'])


def render_source(code: str, settings: IPygmentsCodeConfiguration):
    """Render source with given settings"""
    if settings.lexer == 'auto':
        lexer = guess_lexer(code)
    else:
        lexer = get_lexer_by_name(settings.lexer)
    if lexer is not None:
        formatter = HtmlFormatter(linenos='inline' if settings.display_linenos else None,
                                  nowrap=settings.disable_wrap,
                                  cssclass='source',
                                  style=settings.style)
        return highlight(code, lexer, formatter)
    return None
