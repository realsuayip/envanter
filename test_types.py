import decimal
from typing import Any

from typing_extensions import assert_type

from envanter import EnvironmentParser

env = EnvironmentParser()

# --- parse() ---
assert_type(env.parse("hello", parser=int), int)
assert_type(env.parse("hello", None, parser=int), int | None)
assert_type(env.parse("hello", 1.0, parser=int), float | int)


# --- list() ---
assert_type(env.list("hello"), list[str])
assert_type(env.list("hello", None), list[str] | None)
assert_type(env.list("hello", "none"), list[str] | str)
assert_type(env.list("hello", 1), list[str] | int)
assert_type(env.list("hello", 1.0), list[str] | float)
assert_type(env.list("hello", 1.0, delimiter="$"), list[str] | float)
assert_type(
    env.list("hello", [1, 2], delimiter="$"),
    list[str] | list[int],
)

assert_type(env.list("hello", parser=str), list[str])
assert_type(env.list("hello", parser=int), list[int])
assert_type(env.list("hello", "1", parser=int), list[int] | str)
assert_type(env.list("hello", [1.0], parser=int), list[int] | list[float])
assert_type(env.list("hello", parser=complex, delimiter="$"), list[complex])

# --- choice() ---
assert_type(env.choice("hello", choices=["a", "b"]), str)
assert_type(env.choice("hello", choices=["a", "b"], parser=bool), bool)
assert_type(env.choice("hello", 1, choices=["a", "b"]), str | int)
assert_type(env.choice("hello", 1, choices=["a", "b"], parser=bool), bool | int)

# --- bool() ---
assert_type(env.bool("hello"), bool)
assert_type(env.bool("hello", False), bool)
assert_type(env.bool("hello", None), bool | None)
assert_type(env.bool("hello", 1), bool | int)

# --- str() ---
assert_type(env.str("hello"), str)
assert_type(env.str("hello", "hey"), str)
assert_type(env.str("hello", None), str | None)
assert_type(env.str("hello", 1), str | int)

# --- int() ---
assert_type(env.int("hello"), int)
assert_type(env.int("hello", 1), int)
assert_type(env.int("hello", None), int | None)
assert_type(env.int("hello", 1.0), int | float)

# --- float() ---
assert_type(env.float("hello"), float)
assert_type(env.float("hello", 1.0), float)
assert_type(env.float("hello", None), float | None)
assert_type(env.float("hello", 1), float | int)

# --- decimal() ---
assert_type(env.decimal("hello"), decimal.Decimal)
assert_type(env.decimal("hello", decimal.Decimal(5)), decimal.Decimal)
assert_type(env.decimal("hello", None), decimal.Decimal | None)
assert_type(env.decimal("hello", 1), decimal.Decimal | int)

# --- json() ---
assert_type(env.json("hello"), Any)
assert_type(env.json("hello", 1), Any | int)
assert_type(env.json("hello", None), Any | None)
assert_type(env.json("hello", 1), Any | int)
