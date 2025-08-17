from __future__ import annotations

import enum
import json
import os
from decimal import Decimal
from typing import (
    Any,
    Callable,
    Final,
    Iterable,
    List,
    TypeAlias,
    TypeVar,
    overload,
)

__version__ = "1.3.0"
__all__ = (
    "EnvironmentParser",
    "env",
)

NotSet = enum.Enum("NotSet", "notset")
notset: Final = NotSet.notset

T = TypeVar("T")
V = TypeVar("V")

# this is necessary due to `env.str` pollution
String: TypeAlias = str


class EnvironmentParser:
    """
    Parses environment variables.
    """

    def parse(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        parser: Callable[..., T],
    ) -> T | V:
        """
        Allows fetching values from environment with custom parser
        function to modify it before returning.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :param parser: A callable object that is going to parse the
         variable.
        :raises: ``KeyError``
        :return: Parsed environment variable, or the default value.
        """
        try:
            value = os.environ[name]
        except KeyError:
            if default is notset:
                raise
            return default
        return parser(value)

    @overload
    def list(
        self, name: String, /, default: V | NotSet = notset, *, delimiter: String = ","
    ) -> List[str] | V: ...

    @overload
    def list(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        delimiter: String = ",",
        parser: Callable[..., T],
    ) -> List[T] | V: ...

    def list(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        delimiter: String = ",",
        parser: Callable[..., T] | NotSet = notset,
    ) -> List[str] | List[T] | V:
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
            if default is notset:
                raise
            return default
        if parser is notset:
            return value.split(delimiter)
        return [parser(item) for item in value.split(delimiter)]

    @overload
    def choice(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        choices: Iterable[String],
    ) -> String | V: ...

    @overload
    def choice(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        choices: Iterable[String],
        parser: Callable[..., T],
    ) -> T | V: ...

    def choice(
        self,
        name: String,
        /,
        default: V | NotSet = notset,
        *,
        choices: Iterable[String],
        parser: Callable[..., T] | NotSet = notset,
    ) -> String | T | V:
        """
        Get an environment variable, provided that it complies with the
        choices in the related parameter. Otherwise, throws an exception
        (ValueError), with the available choices.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.

         .. warning::
            If the variable is found but, it does not match any of the choices,
            an exception (``ValueError``) will be raised.

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
            if default is notset:
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
        if parser is notset:
            return value
        return parser(value)

    def bool(self, name: String, /, default: T | NotSet = notset) -> bool | T:
        """
        Get a boolean from environment variable. Allowed values are:
        ``true``, ``1``, ``false`` and ``0``.

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
            if default is notset:
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

    def str(self, name: String, /, default: T | NotSet = notset) -> String | T:
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
            if default is notset:
                raise
            return default

    def int(self, name: String, /, default: T | NotSet = notset) -> int | T:
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
            if default is notset:
                raise
            return default

    def float(self, name: String, /, default: T | NotSet = notset) -> float | T:
        """
        Get a float from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``float``
        :return: A float or the default value.
        """

        try:
            return float(os.environ[name])
        except KeyError:
            if default is notset:
                raise
            return default

    def decimal(self, name: String, /, default: T | NotSet = notset) -> Decimal | T:
        """
        Get a decimal (``decimal.Decimal``) from environment.

        :param name: Name of the environment variable.
        :param default: Optional default value in case the variable is
         not found.
        :raises: ``KeyError``
        :parser: ``decimal.Decimal``
        :return: A decimal or the default value.
        """

        try:
            return Decimal(os.environ[name])
        except KeyError:
            if default is notset:
                raise
            return default

    def json(self, name: String, /, default: T | NotSet = notset) -> Any | T:
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
            if default is notset:
                raise
            return default


env = EnvironmentParser()
