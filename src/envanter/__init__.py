from __future__ import annotations

import decimal
import json
import os
from typing import Any, Callable, Iterable, List, TypeVar, cast, overload

__version__ = "1.2.1"
__all__ = (
    "EnvironmentParser",
    "env",
)


class _Empty:
    def __repr__(self) -> str:
        return "empty"


_empty: Any = _Empty()
_T = TypeVar("_T")
_V = TypeVar("_V")
_str_T = str
_str_F = cast(Callable[..., _T], str)


class EnvironmentParser:
    """
    Parses environment variables.
    """

    def parse(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        parser: Callable[..., _T],
    ) -> _T | _V:
        """
        Allows fetching values from environment with custom parser
        function to modify it before returning.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :param parser: A callable object that is going to parse the
         variable.
        :raises: ``KeyError``
        :parser: ``str`` if no custom parser is specified.
        :return: Parsed environment variable or the default value.
        """
        try:
            value = os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default
        return parser(value)

    @overload
    def list(
        self, name: _str_T, /, default: _V = _empty, *, delimiter: _str_T = ","
    ) -> List[str] | _V: ...

    @overload
    def list(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        delimiter: _str_T = ",",
        parser: Callable[..., _T],
    ) -> List[_T] | _V: ...

    def list(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        delimiter: _str_T = ",",
        parser: Callable[..., _T] = _str_F,
    ) -> List[str] | List[_T] | _V:
        """
        Derive a list from the value of an environment variable.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :param delimiter: Specify a string with which the variable will
         be separated. By default, a comma is used, for example
         'hello,world' would yield a list with 2 members.
        :param parser: Specify a parser callable, which will be mapped
          to resulting list. For example, if you are expecting a list
          of integers, you may pass the ``int`` function.
        :raises: ``KeyError``
        :parser: ``str`` if no custom parser is specified.
        :return: A list of strings or the default value.
        """
        try:
            value = os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default
        return [parser(item) for item in value.split(delimiter)]

    @overload
    def choice(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        choices: Iterable[_str_T],
    ) -> _str_T | _V: ...

    @overload
    def choice(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        choices: Iterable[_str_T],
        parser: Callable[..., _T],
    ) -> _T | _V: ...

    def choice(
        self,
        name: _str_T,
        /,
        default: _V = _empty,
        *,
        choices: Iterable[_str_T],
        parser: Callable[..., _T] = _str_F,
    ) -> _str_T | _T | _V:
        """
        Get an environment variable, provided that it complies with the
        choices in the related parameter. Otherwise, throws an exception
        (ValueError), with the available choices.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found. Notice: if the variable is found but, it does not
         match any of the choices, an exception will be raised.
        :param choices: Iterable of strings that contain the valid choices.
        :param parser: A callable object that is going to parse the
         variable, optional.
        :raises: ``KeyError`` ``ValueError``
        :parser: ``str`` if no custom parser is specified.
        :return: The parsed value of environment variable.
        """

        try:
            value = os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default

        if value not in choices:
            raise ValueError(
                "Got invalid value (%(value)s) from environment,"
                " was expecting one of these: %(expected)s"
                % {
                    "value": value,
                    "expected": tuple(choices),
                }
            )
        return parser(value)

    def bool(self, name: _str_T, /, default: _T = _empty) -> bool | _T:
        """
        Get a boolean from environment variable. Allowed values are:
        'true', '1', 'false' and '0'.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError`` ``ValueError``
        :parser: N/A. Checks if the value is in allowed values
         specified above.
        :return: A boolean or the default value.
        """
        try:
            value = os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default

        value = value.lower()
        truthy, falsy = ("true", "1"), ("false", "0")
        allowed = truthy + falsy

        if value not in allowed:
            raise ValueError(
                "Got invalid value (%(value)s) from environment,"
                " was expecting one of these: %(expected)s"
                % {
                    "value": value,
                    "expected": truthy + falsy,
                }
            )
        return value in truthy

    def str(self, name: _str_T, /, default: _T = _empty) -> _str_T | _T:
        """
        Get a string from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: N/A.
        :return: A string or the default value.
        """
        try:
            return os.environ[name]
        except KeyError:
            if default is _empty:
                raise
            return default

    def int(self, name: _str_T, /, default: _T = _empty) -> int | _T:
        """
        Get an integer from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``int``
        :return: An integer or the default value.
        """
        try:
            return int(os.environ[name])
        except KeyError:
            if default is _empty:
                raise
            return default

    def float(self, name: _str_T, /, default: _T = _empty) -> float | _T:
        """
        Get a float from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``float`` if no custom parser is specified
        :return: A float or the default value.
        """

        try:
            return float(os.environ[name])
        except KeyError:
            if default is _empty:
                raise
            return default

    def decimal(self, name: _str_T, /, default: _T = _empty) -> decimal.Decimal | _T:
        """
        Get a decimal (decimal.Decimal) from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``decimal.Decimal`` if no custom parser is specified
        :return: A decimal or the default value.
        """

        try:
            return decimal.Decimal(os.environ[name])
        except KeyError:
            if default is _empty:
                raise
            return default

    def json(self, name: _str_T, /, default: _T = _empty) -> Any | _T:
        """
        Get Python serialization of a JSON string from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``json.loads``
        :return: The Python serialized version of the JSON,
         or the default value.
        """

        try:
            return json.loads(os.environ[name])
        except KeyError:
            if default is _empty:
                raise
            return default


env = EnvironmentParser()
