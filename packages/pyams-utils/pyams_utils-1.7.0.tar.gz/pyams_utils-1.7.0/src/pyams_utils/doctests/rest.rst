
=======================
PyAMS utils rest module
=======================

PyAMS is using Cornice with a Swagger extension which allows to provide a documentation
for all REST APIs.

This module provides a single view which is used to render OpenAPI specification of all REST
API:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)

    >>> request = DummyRequest('/__api__')
    >>> from pyams_utils.rest import openapi_specification

    >>> from pprint import pprint
    >>> pprint(openapi_specification(request))
    {'basePath': '/',
     'info': {'title': 'PyAMS', 'version': '1.0'},
     'paths': {'/__api__': {'get': {'produces': ['application/json'],
                                    'responses': {'default': {'description': 'UNDOCUMENTED '
                                                                             'RESPONSE'}},
                                    'summary': 'OpenAPI specification'}}},
     'swagger': '2.0'}


Tests cleanup:

    >>> tearDown()
