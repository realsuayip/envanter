Usage
=====

To start using envanter, simply import ``env`` object from the module. This
object will contain various methods which parse environment variables. For
example:

.. code-block:: python

    from envanter import env

    SOME_CONSTANT = env.str("SOME_CONSTANT")

It is possible to specify a default value in case the variable is not found in
the environment:

.. code-block:: python

    SOME_CONSTANT = env.str("SOME_CONSTANT", default="hello")

The type of the default value does not have to comply with the given method,
any arbitrary Python object can be specified.

.. warning::

    If no default is specified, a ``KeyError`` is raised when the environment
    variable is not found. However, each method might throw various exceptions
    depending on their parser function. For example, ``env.decimal`` might
    throw ``decimal.InvalidOperation`` if the variable is not a valid one.
    Check out :doc:`api-reference` for specific information about the parser
    functions used.

Custom parser functions
-----------------------

It is possible to specify a custom parser function, for example:

.. code-block:: pycon

    >>> from envanter import env
    >>> from urllib.parse import urlparse

    >>> env.parse("SOME_URL", parser=urlparse)
    ParseResult(scheme='', netloc='', path='www.example.com', params='', query='', fragment='')

Custom environment parser
-------------------------

The environment parser class is exposed so that you can write your own
subclasses; however, if you are going to create a new subclass, you will be
responsible for maintaining the singleton instance, since ``env`` is bound to
base class.

.. code-block:: python

    from envanter import EnvironmentParser
    from urllib.parse import urlparse, ParseResult


    class CustomEnvironmentParser(EnvironmentParser):
        def url(self, name: str) -> ParseResult:
            value = self.str(name)
            return urlparse(value)


    myenv = CustomEnvironmentParser()
