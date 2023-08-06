
=======================
PyAMS_utils list module
=======================

This small module provides a few helpers to handle lists


Getting unique elements of a list
---------------------------------

The "unique" function returns a list containing unique elements of an input list, in their
original order:

    >>> from pyams_utils.list import unique

    >>> mylist = [1, 2, 3, 2, 1]
    >>> unique(mylist)
    [1, 2, 3]

    >>> mylist = [3, 2, 2, 1, 4, 2]
    >>> unique(mylist)
    [3, 2, 1, 4]

You can also set an 'id' function applied on each element:

    >>> mylist = [1, 2, 3, '2', 4]
    >>> unique(mylist, key=str)
    [1, 2, 3, 4]

    >>> mylist = ['A', 'B', 'b', '2', 4]
    >>> unique(mylist, key=lambda x: str(x).lower())
    ['A', 'B', '2', 4]

The "unique_iter" functions is doing the same thing, but is working with iterators:

    >>> from pyams_utils.list import unique_iter

    >>> mylist = [1, 2, 3, 2, 1]
    >>> list(unique_iter(mylist))
    [1, 2, 3]

    >>> mylist = [3, 2, 2, 1, 4, 2]
    >>> list(unique_iter(mylist))
    [3, 2, 1, 4]

You can also set an 'id' function applied on each element:

    >>> mylist = [1, 2, 3, '2', 4]
    >>> list(unique_iter(mylist, key=str))
    [1, 2, 3, 4]

    >>> mylist = ['A', 'B', 'b', '2', 4]
    >>> list(unique_iter(mylist, key=lambda x: str(x).lower()))
    ['A', 'B', '2', 4]


List random iterator
--------------------

The "random_iter" returns an iterator over elements of an input iterable, selected in random
order:

    >>> from pyams_utils.list import random_iter

    >>> mylist = [1, 2, 3, 2, 1]
    >>> list(random_iter(mylist, 2))
    [..., ...]


Checking iterators for elements
-------------------------------

It's sometimes required to know if an iterator will return at least one element; it's the goal
of the "boolean_iter" function:

    >>> from pyams_utils.list import boolean_iter

    >>> def empty(input):
    ...     yield from input
    >>> mylist = empty(())
    >>> check, myiter = boolean_iter(mylist)
    >>> check
    False
    >>> list(myiter)
    []
    >>> mylist = empty((1,2,3))
    >>> check, myiter = boolean_iter(mylist)
    >>> check
    True
    >>> list(myiter)
    [1, 2, 3]
    >>> list(myiter)
    []

This function can also be used from a Chameleon template with a TALES extension:

    >>> from pyams_utils.list import BooleanIterCheckerExpression
    >>> mylist = empty(())
    >>> expression = BooleanIterCheckerExpression(mylist, None, None)
    >>> expression.render()
    (False, <generator object ... at 0x...>)

    >>> mylist = empty(())
    >>> expression = BooleanIterCheckerExpression(mylist, None, None)
    >>> expression.render(mylist)
    (False, <generator object ... at 0x...>)

    >>> mylist = empty((1,2,3))
    >>> expression = BooleanIterCheckerExpression(mylist, None, None)
    >>> expression.render()
    (True, <generator object ... at 0x...>)
