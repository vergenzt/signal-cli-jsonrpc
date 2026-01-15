from typing import Any, Callable


type NonEmptyTuple[T] = tuple[T, *tuple[T, ...]]


def dict_transform_keys(transform: Callable[[str], str], dct: dict[str, Any]) -> dict[str, Any]:
    return {
        transform(k): (dict_transform_keys(transform, v) if isinstance(v, dict) else v)
        for k, v in dct.items()
    }
