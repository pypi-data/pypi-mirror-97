from typing import Callable, Optional, TypeVar
from os import environ


class ConfigurationError (Exception):
    pass


class MissingConfigurationError (ConfigurationError):
    pass


T = TypeVar('T')


def env(key: str, parser: Callable[[Optional[str]], T], default: Optional[T] = None) -> T:
    try:
        return parser(environ.get(key, default))

    except KeyError:
        raise MissingConfigurationError(f'missing environment var {key}')


def required_str(v: Optional[str]) -> str:
    if v is None:
        raise ValueError

    return v


def optional(v: Optional[T]) -> T:
    return v


def cfg_bool(v: Optional[str]) -> bool:
    if v is None:
        return False

    return v.lower() in ('true', 'yes')
