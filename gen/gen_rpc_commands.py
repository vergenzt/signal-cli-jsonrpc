import ast as a
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import product, takewhile
from operator import or_
from textwrap import dedent, indent
from typing import Iterator, cast, get_args, get_origin

from ast_grep_py import SgNode, SgRoot
from caseutil import to_snake
from ordered_set import OrderedSet

import signal_cli_jsonrpc
from signal_cli_jsonrpc.rpc_command_outputs import RPC_COMMAND_OUTPUT_TYPES

from .utils import (
    SIGNAL_CLI_PATH,
    PyImports,
    annotate_source,
    gen_py_src,
    human_str_list,
    make_required,
    py_dataclass_deco,
    rewrap,
    val,
)

JAVA_COMMAND_FILES = sorted(SIGNAL_CLI_PATH.glob("src/main/java/org/asamk/signal/commands/*.java"))

RPC_COMMAND_IFACE_NAME = "JsonRpcLocalCommand"


EXCLUDED_ARGS: dict[str, set[str]] = defaultdict(
    set,
    {
        "Send": {"message_from_stdin"},
    },
)


def main():
    py_ast = gen()
    py_src = gen_py_src(py_ast)
    print(py_src)


def gen() -> a.Module:
    py_imports = PyImports()

    py_consts: list[a.stmt] = [
        a.parse("type NonEmptyTuple[T] = tuple[T, *tuple[T, ...]]").body[0],
    ]

    py_decls = [
        annotate_source(py_decl, file)
        for file in JAVA_COMMAND_FILES
        if (java_prog_n := SgRoot(file.read_text(), "java").root())
        for java_n in java_prog_n.children()
        if java_n.kind() == "class_declaration"
        if (py_decl := get_py_decl(java_n, py_imports))
    ]

    py_import_decls = [
        a.ImportFrom(mod, [a.alias(n) for n in names], level=0) for mod, names in py_imports.items()
    ]

    py_body = list[a.stmt]()
    py_body.extend(py_import_decls)
    py_body.extend(py_consts)
    py_body.extend(py_decls)
    return a.Module(py_body)


def get_py_decl(java_class_decl_n: SgNode, py_imports: PyImports) -> a.ClassDef | None:
    java_ifces = java_class_decl_n.field("interfaces")
    if not java_ifces or not java_ifces.find(
        kind="type_identifier", regex="^" + RPC_COMMAND_IFACE_NAME + "$"
    ):
        return None

    if not (py_name := get_py_class_name(java_class_decl_n)):
        return None

    if not (py_body := list(get_py_class_body(java_class_decl_n, py_name, py_imports))):
        return None

    output_type = RPC_COMMAND_OUTPUT_TYPES[py_name]
    if get_origin(output_type):  # it's generic
        to_import = get_args(output_type)[0]
        output_type_unqualified = repr(output_type).replace(f"{to_import.__module__}.", "")
    else:
        to_import = output_type
        output_type_unqualified = output_type.__name__

    py_imports.add(
        to_import.__module__.removeprefix(signal_cli_jsonrpc.__name__),
        to_import.__name__,
    )

    py_class_decl = a.ClassDef(
        decorator_list=[py_dataclass_deco(py_imports)],
        name=py_name,
        bases=[py_imports.add(".rpc_session", "RpcCommand")],
        keywords=[
            a.keyword(
                "rpc_output_type",
                a.parse(output_type_unqualified, mode="eval").body,
            )
        ],
        body=py_body,
    )

    return py_class_decl


def get_py_class_name(java_class_decl_n: SgNode) -> str | None:
    java_name_decl = java_class_decl_n.find(
        kind="method_declaration",
        pattern='@Override public String getName() { return "$NAME"; }',
    )
    if not java_name_decl:
        return None

    java_name = java_name_decl["NAME"].text()
    py_name = java_name[0].upper() + java_name[1:]  # camelCase -> PascalCase
    return py_name


@dataclass
class ArgGroup:
    mutex: bool
    required: bool
    argnames: OrderedSet[str]


def get_py_class_body(
    java_class_decl_n: SgNode, py_class_name: str, py_imports: PyImports
) -> Iterator[a.stmt]:
    java_subp_decl = java_class_decl_n.find(
        kind="method_declaration",
        pattern="@Override public void attachToSubparser($$$) { $$$BODY }",
    )
    if not java_subp_decl:
        yield from []
        return

    java_body = filter(SgNode.is_named, val(java_subp_decl.field("body")).children())

    py_cmd_help: str | None = None
    py_args = dict[str, a.AnnAssign]()
    py_arg_helps = dict[str, str]()
    py_arg_groups = dict[str, ArgGroup](
        {"subparser": ArgGroup(mutex=False, required=False, argnames=OrderedSet(()))}
    )

    for java_stmt in java_body:
        if help_stmt := java_stmt.find(pattern='subparser.help("$HELP")'):
            assert help_stmt.parent() == java_stmt
            py_cmd_help = help_stmt["HELP"].text()

        elif java_add_arg_call := java_stmt.find(pattern="$OBJ.addArgument($$$)"):
            py_arg_name, py_arg, py_arg_help = get_py_arg_decl(
                java_stmt, java_add_arg_call, py_imports
            )
            if py_arg_name in EXCLUDED_ARGS[py_class_name]:
                continue
            else:
                py_args[py_arg_name] = py_arg
                if py_arg_help:
                    py_arg_helps[py_arg_name] = py_arg_help

                obj_name = java_add_arg_call["OBJ"].text()
                py_arg_groups[obj_name].argnames.add(py_arg_name)

        elif java_stmt.kind() == "local_variable_declaration":
            assert (mutex_decl := java_stmt.find(pattern="subparser.addMutuallyExclusiveGroup()"))

            var_name = val(val(java_stmt.field("declarator")).field("name")).text()
            group_required = val(mutex_decl.parent()).matches(pattern="$_.required(true)")
            group = ArgGroup(mutex=True, required=group_required, argnames=OrderedSet(()))
            py_arg_groups[var_name] = group

            assert mutex_decl.ancestors()[int(group_required)].kind() == "variable_declarator"

        else:
            raise NotImplementedError(
                f"Unhandled statement from attachToSubparser(...): {java_stmt.text()}"
            )

    # check if EXCLUDED_ARGS reduced a mutex down to one arg, meaning:
    #  a) if it's required then its sole arg must now be non-optional, and
    #  b) we can remove it from consideration
    moot_mutex_names = [
        group_name
        for group_name, group in py_arg_groups.items()
        if group.mutex and len(group.argnames) == 1
    ]
    for group_name in moot_mutex_names:
        # destroy the mutex
        group = py_arg_groups.pop(group_name)
        py_arg = py_args[py_arg_name := group.argnames.pop()]
        py_arg_groups["subparser"].argnames.add(py_arg_name)
        assert not group.argnames

        # if the singleton mutex group we just removed was required,
        # then make its sole arg required
        if group.required:
            py_arg = py_args[py_arg_name] = make_required(py_arg, py_imports)

    py_mutex_groups = {name: group for name, group in py_arg_groups.items() if group.mutex}
    assert all(len(group.argnames) > 1 for group in py_mutex_groups.values())

    # sort args names so that args without defaults come first
    py_arg_names_ordered = sorted(py_args.keys(), key=lambda n: py_args[n].value is not None)

    if py_class_doc := get_py_class_docstring(
        py_cmd_help, py_mutex_groups, py_arg_helps, py_arg_names_ordered
    ):
        yield py_class_doc

    # emit the argument (i.e. dataclass field) definitions
    yield from (py_args[name] for name in py_arg_names_ordered)

    # if there are mutex groups, then:
    #  a) overload __init__ methods to provide type hints, and
    #  b) validate mutual exclusions at runtime in __post_init__.
    if py_mutex_groups:
        yield from get_py_class_init_overloads(
            py_arg_names_ordered, py_args, py_arg_groups, py_imports
        )

        yield get_py_class_init_impl(py_mutex_groups, py_imports)


def get_py_class_docstring(
    py_cmd_help: str | None,
    py_mutex_groups: dict[str, ArgGroup],
    py_arg_helps: dict[str, str],
    py_arg_names_ordered: list[str],
) -> a.stmt | None:
    if py_cmd_help or py_mutex_groups or py_arg_helps:
        help_paras: list[str] = []

        if py_cmd_help:
            help_paras.append(rewrap(py_cmd_help))

        if py_mutex_groups:
            note_lines = list[str]()
            for mutex in py_mutex_groups.values():
                arg_strs = [f":attr:`{n}`" for n in mutex.argnames]
                if mutex.required:
                    args_str = human_str_list(arg_strs, "or")
                    note = f" - Exactly one of {args_str} is required."
                else:
                    args_str = human_str_list(arg_strs, "and")
                    note = f" - {args_str} are mutually exclusive."
                note_lines.append(note)

            note_lines.insert(0, "Note" + (len(py_mutex_groups) > 1) * "s" + ":")
            help_paras.append("\n".join(note_lines))

        if py_arg_helps:
            # use new sort order (args with defaults pushed to the end) for arg helptext order
            py_args_help = "\n".join(
                rewrap(
                    f":param {arg_name}: {py_arg_helps.get(arg_name, '')}", subsequent_indent="    "
                )
                for arg_name in py_arg_names_ordered
            )
            help_paras.append(py_args_help)

        py_class_help = "\n" + "\n\n".join(filter(None, help_paras)) + "\n"
        return a.Expr(a.Constant(indent(py_class_help, " " * 4) + " " * 4))


def get_py_class_init_overloads(
    py_arg_names_ordered: list[str],
    py_args: dict[str, a.AnnAssign],
    py_arg_groups: dict[str, ArgGroup],
    py_imports: PyImports,
) -> list[a.FunctionDef]:
    # what are the possible contributions of each group to the arguments list?
    arg_group_possibilities = dict[str, list[dict[str, a.AnnAssign]]]()

    for group_name, group in py_arg_groups.items():
        arg_group_possibilities[group_name] = group_possibilities = list[dict[str, a.AnnAssign]]()

        # only one argument from this group may be specified
        if group.mutex:
            # allow this group to contribute NO args to the final signature (if not required)
            if not group.required:
                group_possibilities.append(dict())
            # or exactly one of each arg (in which case the arg is "required" for the overload to apply)
            for arg_name in group.argnames:
                arg_as_required = make_required(py_args[arg_name], py_imports)
                group_possibilities.append({arg_name: arg_as_required})

        else:
            # not mutually exclusive; no dependencies between args so they can all be in one "possibility"
            group_possibilities.append({arg_name: py_args[arg_name] for arg_name in group.argnames})

    init_overloads = list[a.FunctionDef]()

    overload_args_dicts: list[dict[str, a.AnnAssign]] = [
        reduce(or_, group_args_dicts)
        for group_args_dicts in product(*arg_group_possibilities.values())
    ]
    for overload_args_dict in overload_args_dicts:
        overload_py_args: list[a.AnnAssign] = [
            py_arg for name in py_arg_names_ordered if (py_arg := overload_args_dict.get(name))
        ]
        overload_args = a.arguments(
            args=[a.arg("self")],
            kwonlyargs=[
                a.arg(cast(a.Name, py_arg.target).id, py_arg.annotation)
                for py_arg in overload_py_args
            ],
            kw_defaults=[a.Constant(...) if py_arg.value else None for py_arg in overload_py_args],
        )
        init_overloads.append(
            a.FunctionDef(
                decorator_list=[py_imports.add("typing", "overload")],
                name="__init__",
                args=overload_args,
                body=[a.Expr(a.Constant(...))],
                lineno=0,
            )
        )

    return init_overloads


def get_py_class_init_impl(
    py_mutex_groups: dict[str, ArgGroup], py_imports: PyImports
) -> a.FunctionDef:
    py_imports.add("dataclasses", "fields")
    py_imports.add("dataclasses", "MISSING")

    init_impl = a.parse(
        dedent("""
            def __init__(self, **kwargs):
                self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
                self.__dict__.update(kwargs)
        """)
    ).body[0]
    assert isinstance(init_impl, a.FunctionDef)

    for mutex in py_mutex_groups.values():
        args_repr = repr(list(mutex.argnames))
        if mutex.required:
            init_impl.body += a.parse(
                dedent(f"""
                    match len(kwargs.keys() & (args := {args_repr})):
                        case 0:
                            raise ValueError(f"One of {{args!r}} is required!")
                        case 1:
                            pass
                        case _:
                            raise ValueError(f"Arguments {{args!r}} are mutually exclusive!")
                """)
            ).body
        else:
            init_impl.body += a.parse(
                dedent(f"""
                    match len(kwargs.keys() & (args := {args_repr})):
                        case 0 | 1:
                            pass
                        case _:
                            raise ValueError(f"Arguments {{args!r}} are mutually exclusive!")
                """)
            ).body

    return init_impl


def get_py_arg_decl(
    java_stmt: SgNode, java_add_arg_call: SgNode, py_imports: PyImports
) -> tuple[str, a.AnnAssign, str]:
    java_opts = val(java_add_arg_call.field("arguments"))
    first_long_opt = val(java_opts.find(kind="string_fragment", regex="^(--)?[a-z]")).text()

    py_arg_name: str = to_snake(first_long_opt.lstrip("-"))
    py_arg_annot: a.expr = a.Name("str")
    py_arg_value: a.expr | None = None
    py_arg_can_be_none: bool = True
    py_arg_help: str = ""

    java_arg_addl_calls = {
        val(chained_call.field("name")).text(): (
            val(chained_call.field("arguments")).text()[1:-1].strip()
        )
        for chained_call in takewhile(
            lambda n: n.kind() == "method_invocation", java_add_arg_call.ancestors()
        )
    }

    while java_arg_addl_calls:
        match java_arg_addl_calls:
            case {"help": doc_expr, **rest}:
                py_arg_help = " ".join(doc_expr.strip().split()).replace('" + "', "").strip('"')
                java_arg_addl_calls = rest
            case {"action": "Arguments.storeTrue()", **rest}:
                py_arg_annot = a.Name("bool")
                py_arg_value = a.Constant(False)
                py_arg_can_be_none = False
                java_arg_addl_calls = rest
            case {"choices": choices, **rest}:
                py_arg_annot = a.Subscript(
                    py_imports.add("typing", "Literal"),
                    a.Constant(a.literal_eval(choices)),
                )
                java_arg_addl_calls = rest
            case {"type": type, **rest}:
                match type.removesuffix(".class"):
                    case "int" | "long":
                        py_arg_annot = a.Name("int")
                    case "Boolean":
                        py_arg_annot = a.Name("bool")
                    case "Arguments.enumStringType(MessageRequestResponseType.class)":
                        rest["choices"] = '"accept", "delete"'
                java_arg_addl_calls = rest
            case {"nargs": '"*"', **rest}:
                py_arg_name += "s"
                py_arg_annot = a.Subscript(
                    a.Name("tuple"), a.Tuple([py_arg_annot, a.Constant(...)])
                )
                py_arg_can_be_none = False
                py_arg_value = a.Tuple([])
                java_arg_addl_calls = rest
            case {"nargs": '"+"', **rest}:
                py_arg_name += "s"
                py_arg_annot = a.Subscript(a.Name("NonEmptyTuple"), py_arg_annot)
                py_arg_can_be_none = False
                java_arg_addl_calls = rest
            case {"required": "true", **rest}:
                py_arg_can_be_none = False
                java_arg_addl_calls = rest
            case _:
                raise ValueError(f"Don't know how to handle arg calls: {java_arg_addl_calls}")

    if py_arg_can_be_none:
        py_arg_annot = a.BinOp(py_arg_annot, a.BitOr(), a.Constant(None))
        py_arg_value = py_arg_value or a.Constant(None)

    py_arg = a.AnnAssign(
        target=a.Name(py_arg_name),
        annotation=py_arg_annot,
        value=py_arg_value,
        simple=1,
    )
    return py_arg_name, py_arg, py_arg_help


if __name__ == "__main__":
    main()
