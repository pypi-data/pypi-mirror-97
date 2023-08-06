
==========================
PyAMS_utils factory module
==========================

Instead of directly using a class as an object factory, the object of this module is to
let you create an object based on an interface. The first step is to create an object
implementing this interface, and then to register it as a factory:

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from zope.interface import Interface, implementer
    >>> class IMyInterface(Interface):
    ...     '''Custom marker interface'''

    >>> @implementer(IMyInterface)
    ... class MyClass:
    ...    '''Class implementing my interface'''

    >>> from pyams_utils.factory import register_factory
    >>> register_factory(IMyInterface, MyClass)

You can also register a named factory:

    >>> register_factory(IMyInterface, MyClass, name='my-factory')

Factory registry can also be handle by a decorator called "factory_config":

    >>> from pyams_utils.factory import factory_config
    >>> @factory_config(IMyInterface)
    ... class MyClass(object):
    ...     '''Class implementing my interface'''

A class declared as factory for a specific interface automatically implements the given interface.
You can also provide a tuple or set of interfaces in "factory_config()" decorator.

When a factory is registered, you can look for a factory:

    >>> from pyams_utils.factory import get_object_factory
    >>> factory = get_object_factory(IMyInterface)
    >>> factory
    <pyams_utils.factory.register_factory.<locals>.Temp object at 0x...>
    >>> if factory is not None:
    ...     myobject = factory()
    ... else:
    ...     myobject = object()

Named factories are used in the same way:

    >>> factory = get_object_factory(IMyInterface, name='my-factory')
    >>> factory
    <pyams_utils.factory.register_factory.<locals>.Temp object at 0x...>

By registering their own objects factories, extension packages can easily provide their
own implementation of any PyAMS interface handled by factories.


Tests cleanup:

    >>> tearDown()
