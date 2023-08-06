
=======================
PyAMS_utils zodb module
=======================

PyAMS_utils provides a few helpers to manage ZODB connections.

    >>> import pprint

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)


Persistent connection adapter
-----------------------------

This adapter provides an adapter to any persistent object:

    >>> from ZODB.interfaces import IConnection
    >>> from transaction.interfaces import ITransactionManager
    >>> from pyams_utils.zodb import ZODBConnection
    >>> conn = ZODBConnection()
    >>> conn
    <pyams_utils.zodb.ZODBConnection object at 0x...>

    >>> with conn as root:
    ...     pprint.pprint((root, IConnection(root), conn.connection, conn.db, conn.storage))
    ({},
     <Connection at ...>,
     <Connection at ...>,
     <ZODB.DB.DB object at 0x...>,
     <ZODB.MappingStorage.MappingStorage object at 0x...>)

    >>> with conn as root:
    ...     pprint.pprint(ITransactionManager(root))
    <transaction._manager.TransactionManager object at 0x...>


ZODB connections vocabulary
---------------------------

A vocabulary of available ZODB connections is available:

    >>> from zope.interface import implementer, Interface
    >>> from zope.schema import Choice
    >>> from pyams_utils.interfaces import ZODB_CONNECTIONS_VOCABULARY_NAME

    >>> class IMyContent(Interface):
    ...     zodb = Choice(title='ZODB connection',
    ...                   vocabulary=ZODB_CONNECTIONS_VOCABULARY_NAME)

    >>> from persistent import Persistent
    >>> from zope.schema.fieldproperty import FieldProperty
    >>> @implementer(IMyContent)
    ... class MyContent(Persistent):
    ...     zodb = FieldProperty(IMyContent['zodb'])

    >>> content = MyContent()
    >>> content.zodb = ''
    >>> content.zodb
    ''
    >>> content.zodb = 'missing'
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.ConstraintNotSatisfied: ('missing', 'zodb')

You can also get a connection from settings:

    >>> from pyams_utils.zodb import get_connection_from_settings
    >>> get_connection_from_settings()
    <Connection at ...>

A vocabulary is available to list registered ZEO connections:

    >>> from pyams_utils.zodb import ZEOConnectionVocabulary
    >>> vocabulary = ZEOConnectionVocabulary()


Using volatile properties
-------------------------

Volatile properties are using volatile attributes of persistent object to save data which
is not stored into ZODB:

    >>> from pyams_utils.zodb import volatile_property
    >>> class MyContent(Persistent):
    ...     @volatile_property
    ...     def value(self):
    ...         pprint.pprint("Getting value...")
    ...         return 1

    >>> content = MyContent()
    >>> content.value
    'Getting value...'
    1

Calling property another time just returns value of volatile attribute:

    >>> content.value
    1

If you delete a volatile property, it's matching attribute is removed:

    >>> del content.value
    >>> content.value
    'Getting value...'
    1


Managing ZEO connections
------------------------

PyAMS provides an helper class to manage ZEO connections; these connections can be defined as
persistent utilities stored into ZODB:

    >>> from pyams_utils.zodb import ZEOConnection
    >>> connection = ZEOConnection()
    >>> pprint.pprint(connection.get_settings())
    {'blob_dir': None,
     'name': None,
     'password': None,
     'server_name': 'localhost',
     'server_port': 8100,
     'server_realm': None,
     'shared_blob_dir': False,
     'storage': '1',
     'username': None}

    >>> connection.update({'name': 'zeo_connection'})
    >>> pprint.pprint(connection.get_settings())
    {'blob_dir': None,
     'name': 'zeo_connection',
     'password': None,
     'server_name': 'localhost',
     'server_port': 8100,
     'server_realm': None,
     'shared_blob_dir': False,
     'storage': '1',
     'username': None}

    >>> connection.get_connection(wait_timeout=1)
    Traceback (most recent call last):
    ...
    ZEO.Exceptions.ClientDisconnected: timed out waiting for connection


Tests cleanup:

    >>> tearDown()
