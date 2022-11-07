# envanter

Yet another environment parser.

## Usage

```python
>>> from envanter import env

>>> env.str("SOME_STRING")
'my string'

>>> env.int("SOME_INTEGER")
7

>>> env.float("SOME_FLOAT")
3.14

>>> env.decimal("SOME_DECIMAL")
decimal.Decimal("2.71")

>>> env.json("SOME_JSON")
{"hello": "world"}

>>> env.bool("some-bool")
True

>>> env.bool("some-bool-but-wrong-keyword")
AssertionError: Allowed values are: ('true', '1', 'false', '0')

>>> env.str("nothing", "something")
'something'

>>> env.str("nothing")
KeyError: 'nothing'
```

### Custom parser function

````python
>>> from envanter import env
>>> from urllib.parse import urlparse

>>> env.parse("SOME_URL", parser=urlparse)
ParseResult(scheme='', netloc='', path='www.example.com', params='', query='', fragment='')
````
