import ast as a
import builtins as b
from collections import defaultdict
from copy import copy, deepcopy
from functools import partial
from pathlib import Path
from subprocess import check_output
from textwrap import dedent, indent, wrap
from typing import Literal, Sequence

sh = partial(check_output, text=True)

_wrap = partial(wrap, break_long_words=False, break_on_hyphens=False)


def human_str_list(parts: Sequence[str], conj: Literal["or", "and"]) -> str:
    return ", ".join(parts[:-1]) + ("," if len(parts) > 2 else "") + f" {conj} " + parts[-1]


def make_required(py_arg: a.AnnAssign, py_imports: PyImports) -> a.AnnAssign:
    # start with a copy
    py_arg = copy(py_arg)

    # remove default value.
    # n.b.:
    # - `.value = None` means no default
    # - `.value = ast.Constant(None)` means default of `None`
    py_arg.value = None

    # and remove None or empty tuple from allowed values
    match py_arg.annotation:
        # `bool` -> `Literal[True]`
        case a.Name("bool"):
            py_arg.annotation = a.Subscript(py_imports.add("typing", "Literal"), a.Constant(True))
        # `<type> | None` -> `<type>`
        case a.BinOp(main_type, a.BitOr(), a.Constant(None)):
            py_arg.annotation = main_type
        # `tuple[<type>, ...]` -> `NonEmptyTuple[<type>]`
        case a.Subscript(a.Name("tuple"), a.Tuple([main_type, a.Constant(b.Ellipsis)])):
            py_arg.annotation = a.Subscript(a.Name("NonEmptyTuple"), main_type)

    return py_arg


def rewrap(help: str, **kw) -> str:
    # choose wrapping col which maximizes my aesthetic pleasure (no short final lines)
    return "\n".join(
        max(
            (_wrap(help, c, **kw) for c in [80, 90, 100, 70]),
            key=lambda lines: len(lines[-1]) > 25,
        )
    )


def val[T](val: T | None) -> T:
    "Helper to inline type-narrow an optional value"
    assert val, f"expected {val} to be truthy!"
    return val


class PyImports(defaultdict[str, set[str]]):
    def __init__(self, **kw):
        super().__init__(set, **kw)

    def add(self, mod: str, name: str) -> a.Name:
        """Adds a new name to be imported, and returns it"""
        self[mod].add(name)
        return a.Name(name)


def py_dataclass_deco(py_imports: PyImports) -> a.expr:
    return a.Call(
        func=py_imports.add("dataclasses", "dataclass"),
        keywords=[
            a.keyword("frozen", a.Constant(True)),
            a.keyword("kw_only", a.Constant(True)),
        ],
    )


GIT_ROOT = Path(sh(["git", "rev-parse", "--show-toplevel"]).strip())


def git_submodule_config(key: str) -> str:
    return sh(["git", "config", "--file", GIT_ROOT / ".gitmodules", key]).strip()


SIGNAL_CLI_PATH = GIT_ROOT / git_submodule_config("submodule.signal-cli.path")
SIGNAL_CLI_URL = git_submodule_config("submodule.signal-cli.url")


def normalize_docstring(docstr: str) -> str:
    if "\n" in docstr:
        return indent("\n" + dedent(docstr).strip(), "    ") + "\n    "
    else:
        return docstr


def annotate_source(py_decl: a.ClassDef, src: Path) -> a.ClassDef:
    """Add a comment as the first line of the class body"""

    src_rel = src.relative_to(SIGNAL_CLI_PATH)
    src_sha = sh(["git", "rev-list", "-1", "HEAD", "--", src_rel], cwd=SIGNAL_CLI_PATH).strip()
    src_url = f"{SIGNAL_CLI_URL}/blob/{src_sha}/{src_rel}"
    src_doc = f"*[generated from [Java source]({src_url})]*"

    py_decl = deepcopy(py_decl)
    match py_decl.body:
        case [a.Expr(a.Constant(str() as docstring)), *_]:
            py_decl.body[0] = a.Expr(
                a.Constant(normalize_docstring(dedent(docstring).strip() + "\n\n" + src_doc))
            )
        case _:
            py_decl.body.insert(0, a.Expr(a.Constant(normalize_docstring(src_doc))))

    return py_decl


def gen_py_src(py_ast: a.AST) -> str:
    py_src = a.unparse(py_ast)
    py_src = sh(["ruff", "format", "-"], input=py_src)
    py_src = sh(["ruff", "check", "--quiet", "--extend-select=I", "--fix", "-"], input=py_src)
    py_src = py_src.rstrip()
    return py_src
