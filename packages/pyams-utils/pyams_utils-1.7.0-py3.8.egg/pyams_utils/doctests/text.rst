
=======================
PyAMS_utils text module
=======================

PyAMS_utils.text is a small module dedicated to small text management functions.

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)

    >>> from pyramid_chameleon.zpt import renderer_factory
    >>> config.add_renderer('.pt', renderer_factory)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()


Truncating text
---------------

*truncate* is a TALES extension used to truncate text:

    >>> from pyams_utils.text import TruncateCharsTalesExtension
    >>> context, request, view = object(), DummyRequest(), object()
    >>> extension = TruncateCharsTalesExtension(context, request, view)
    >>> extension.render('This is my very very long text', 15, 3)
    'This is my&#133;'

    >>> template = os.path.join(temp_dir, 'truncate.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:truncate('This is my text to truncate', 15)}</div>")

    >>> from pyramid.renderers import render
    >>> render(template, {'request': request})
    '<div>This is my&#133;</div>'

    >>> template = os.path.join(temp_dir, 'truncate-empty.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:truncate('', 15)}</div>")

    >>> render(template, {'request': request})
    '<div></div>'


Text rendering
--------------

Several renderers are available to render text to HTML, based on named adapters
to *IHTMLRenderer* interface:

    >>> from pyams_utils.text import text_to_html

    >>> text_to_html('Basic raw text')
    'Basic raw text'
    >>> text_to_html('Basic raw text\nwith line breaks', 'raw')
    'Basic raw text\nwith line breaks'
    >>> text_to_html('Basic raw text\nwith line breaks', 'text')
    'Basic raw text<br />\nwith line breaks'
    >>> text_to_html("Text with 'quotes'", 'js')
    "Text with \\'quotes\\'"
    >>> text_to_html("ReStructured **text**", 'rest')
    '<p>ReStructured <strong>text</strong></p>\n'

Some renderers can receive additional arguments:

    >>> import pprint
    >>> from pyams_utils.context import capture_stderr
    >>> with capture_stderr(text_to_html, "ReStructured **text**", 'rest', settings={'dump_settings': True}) as (result, errors):
    ...     pprint.pprint(errors)
    ('\n'
     '::: Runtime settings:\n'
     ...

    >>> text_to_html("Markdown *text*", 'markdown')
    '<p>Markdown <em>text</em></p>'

Please note that you can also provide several renderers which will be called sequentially:

    >>> text_to_html("This is JS 'text' to *render*", 'rest;js')
    "<p>This is JS \\'text\\' to <em>render</em></p>\n"


A TALES extension called "html" is available to include renderers into page templates:

    >>> from pyams_utils.text import HTMLTalesExtension
    >>> extension = HTMLTalesExtension(context, request, view)
    >>> extension.render('Basic raw text', 'text')
    'Basic raw text'
    >>> extension.render(123, 'text')
    '123'
    >>> extension.render(None)
    ''

Context is extracted from request if not specified explicitly:

    >>> extension.render()
    '<object object at 0x...>'

You have to provide a custom HTML renderer to render an object directly:

    >>> from zope.interface import implementer, Interface
    >>> class IMyInterface(Interface):
    ...     """Marker interface"""

    >>> @implementer(IMyInterface)
    ... class MyClass:
    ...     name = 'My class name'
    ...     def __repr__(self):
    ...         return self.name

    >>> from pyams_utils.adapter import ContextRequestAdapter
    >>> class MyCustomRenderer(ContextRequestAdapter):
    ...     def render(self):
    ...         return str(self.context)

    >>> from pyams_utils.interfaces.text import IHTMLRenderer
    >>> config.registry.registerAdapter(MyCustomRenderer, (IMyInterface, DummyRequest), IHTMLRenderer)

    >>> my_object = MyClass()
    >>> extension.render(my_object)
    'My class name'

    >>> template = os.path.join(temp_dir, 'html.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:html(context)}</div>")

    >>> from pyramid.renderers import render
    >>> render(template, {'context': my_object, 'request': request})
    '<div>My class name</div>'

A vocabulary is available to make a selection between all available renderers:

    >>> from pyams_utils.text import RenderersVocabulary
    >>> vocabulary = RenderersVocabulary()


Breaking lines
--------------

*br* is another TALES extension which can be used to convert special characters in a text string to
line breaks, eventually adding start and end tags:

    >>> from pyams_utils.text import BrTalesExtension
    >>> extension = BrTalesExtension(context, request, view)
    >>> extension.render(None)
    ''
    >>> extension.render('This is my|text to break')
    'This is my<br  />text to break'
    >>> extension.render('This is my|text to break', css_class='hidden-xs')
    'This is my<br class="hidden-xs" />text to break'
    >>> extension.render('This is my|text to break', css_class='hidden-xs', start_tag='div', end_tag='p')
    '<div>This is my</div><br class="hidden-xs" /><p>text to break</p>'

    >>> template = os.path.join(temp_dir, 'break.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:br('This is my|text to break')}</div>")

    >>> from pyramid.renderers import render
    >>> render(template, {'request': request})
    '<div>This is my<br  />text to break</div>'

You can specify the character used to handle line breaks:

    >>> template2 = os.path.join(temp_dir, 'break-2.pt')
    >>> with open(template2, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:br('This is my\ntext to break', character='\\n')}</div>")
    >>> render(template2, {'request': request})
    '<div>This is my<br  />text to break</div>'


Tests cleanup:

    >>> tearDown()
