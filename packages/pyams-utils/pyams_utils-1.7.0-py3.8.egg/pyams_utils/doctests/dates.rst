
=======================
PyAMS utils date module
=======================

Dates functions are used to convert dates from/to string representation:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)

    >>> import pytz
    >>> from datetime import datetime
    >>> from pyams_utils import date
    >>> gmt = pytz.timezone('GMT')
    >>> now = datetime.fromtimestamp(1205000000, gmt)
    >>> now
    datetime.datetime(2008, 3, 8, 18, 13, 20, tzinfo=<StaticTzInfo 'GMT'>)

You can get an unicode representation of a date in ASCII format using 'unidate' fonction ; date is
converted to GMT:

    >>> udate = date.unidate(now)
    >>> udate
    '2008-03-08T18:13:20+00:00'

'parse_date' can be used to convert ASCII format into datetime:

    >>> ddate = date.parse_date(udate)
    >>> ddate
    datetime.datetime(2008, 3, 8, 18, 13, 20, tzinfo=<StaticTzInfo 'GMT'>)

'date_to_datetime' can be used to convert a 'date' type to a 'datetime' value ; if a 'datetime' value
is used as argument, it is returned 'as is':

    >>> ddate.date()
    datetime.date(2008, 3, 8)
    >>> date.date_to_datetime(ddate)
    datetime.datetime(2008, 3, 8, 18, 13, 20, tzinfo=<StaticTzInfo 'GMT'>)
    >>> date.date_to_datetime(ddate.date())
    datetime.datetime(2008, 3, 8, 0, 0)


Timestamp TALES extension
-------------------------

The *timestamp* TALES extension can be used to include an object timestamp into a Chameleon
template:

    >>> from pyramid_chameleon.zpt import renderer_factory
    >>> config.add_renderer('.pt', renderer_factory)

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()

    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.dublincore.interfaces import IZopeDublinCore
    >>> from zope.dublincore.annotatableadapter import ZDCAnnotatableAdapter
    >>> config.registry.registerAdapter(ZDCAnnotatableAdapter, (IAttributeAnnotatable, ),
    ...                                 IZopeDublinCore)

    >>> template = os.path.join(temp_dir, 'timestamp.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:timestamp(context)}</div>")

    >>> from zope.interface import implementer, Interface
    >>> class IMyContent(Interface):
    ...     """Custom marker interface"""

    >>> @implementer(IMyContent, IAttributeAnnotatable)
    ... class MyContent:
    ...     """Custom class"""
    >>> my_content = MyContent()

    >>> zdc = IZopeDublinCore(my_content)
    >>> zdc.modified = zdc.created = datetime.utcnow()

    >>> from pyramid.renderers import render
    >>> output = render(template, {'context': my_content, 'request': DummyRequest()})
    >>> output == '<div>{}</div>'.format(zdc.modified.timestamp())
    True

    >>> template = os.path.join(temp_dir, 'timestamp-iso.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${structure:tales:timestamp(context, 'iso')}</div>")

    >>> output = render(template, {'context': my_content, 'request': DummyRequest()})
    >>> output == '<div>{}</div>'.format(zdc.modified.isoformat())
    True

Using this TALES extension on an object which doesn't support dublincore interface just returns
current timestamp:

    >>> content = object()
    >>> render(template, {'request': DummyRequest(context=content)})
    '<div>...-...-...T...:...:...+00:00</div>'


Timezones handling
------------------

Timezones handling gave me headaches at first. I finally concluded that the best way (for me !) to handle
TZ data was to store every datetime value in GMT timezone.
As far as I know, there is no easy way to know the user's timezone from his request settings. So you can:
- store this timezone in user's profile,
- define a static server's timezone
- create and register a ServerTimezoneUtility to handle server default timezone.

My current default user's timezone is set to 'Europe/Paris'; you should probably update this setting in
'timezone.py' if you are located elsewhere.

    >>> from pyams_utils import timezone
    >>> timezone.tztime(ddate)
    datetime.datetime(2008, 3, 8, 18, 13, 20, tzinfo=<StaticTzInfo 'GMT'>)

'gmtime' function can be used to convert a datetime to GMT:

    >>> timezone.gmtime(now)
    datetime.datetime(2008, 3, 8, 18, 13, 20, tzinfo=<StaticTzInfo 'GMT'>)


Tests cleanup:

    >>> tearDown()
