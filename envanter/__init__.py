import decimal
import json
import os

__version__ = "1.0.0"
__all__ = ["env", "EnvironmentParser"]

_empty = object()


def _construct(parser):
    def process(self, name, default=_empty):
        return self.parse(name, default, parser)

    return process


class EnvironmentParser:
    def parse(self, name, default=_empty, parser=None):  # noqa
        try:
            value = os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default

        if parser is not None:
            return parser(value)

        return value

    def list(self, name, default=_empty, *, delimiter=",") -> list:
        return self.parse(name, default, lambda v: v.split(delimiter))

    def bool(self, name, default=_empty) -> bool:  # noqa
        value = self.parse(name, default=default)

        if isinstance(value, bool):
            return value

        value = value.lower()
        truthy, falsy = ("true", "1"), ("false", "0")
        allowed = truthy + falsy
        assert value in allowed, "Allowed values are: %s" % str(allowed)
        return value in truthy

    str = _construct(str)
    int = _construct(int)
    float = _construct(float)
    decimal = _construct(decimal.Decimal)
    json = _construct(json.loads)


env = EnvironmentParser()
