from functools import partial
from textwrap import wrap


_wrap = partial(wrap, break_long_words=False, break_on_hyphens=False)


def rewrap(help: str, **kw) -> str:
    # choose wrapping col which maximizes my aesthetic pleasure (no short final lines)
    return "\n".join(
        max(
            (_wrap(help, c, **kw) for c in [80, 90, 100, 70]), key=lambda lines: len(lines[-1]) > 25
        )
    )


def format_docstring(doc: str) -> str:
    if "\n" in doc:
        return f'"""\n{doc}\n"""'  # put newline between doc and """ if multiline
    else:
        return f'"{doc}"'


def val[T](val: T | None) -> T:
    "Helper to inline type-narrow an optional value"
    assert val
    return val
