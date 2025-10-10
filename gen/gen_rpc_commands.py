# everything that 'implements JsonRpcLocalCommand'
import sys
from collections import defaultdict
from dataclasses import dataclass, replace
from itertools import chain, groupby, product, takewhile
from pathlib import Path
from textwrap import indent

from ast_grep_py import Relation, SgNode, SgRoot

from .utils import format_docstring, rewrap, val

JAVA_COMMAND_FILES = sorted(
    Path(__file__).parent.glob("../signal-cli/src/main/java/org/asamk/signal/commands/*.java")
)

RPC_COMMAND_IFACE_NAME = "JsonRpcLocalCommand"


EXCLUDED_ARGS: dict[str, set[str]] = defaultdict(
    set,
    {
        "Send": {"message_from_stdin"},
    },
)


def gen():
    print("from dataclasses import MISSING, dataclass, fields")
    print("from typing import Literal, Optional, overload")
    print()
    print("from .rpc_session import RpcCommand")
    print()
    print()
    print("type NonEmptyTuple[T] = tuple[T, *tuple[T, ...]]")
    print()
    print()

    for file in JAVA_COMMAND_FILES:
        process_file(SgRoot(file.read_text(), "java").root())


def process_file(root: SgNode):
    class_decl = root.find(
        kind="class_declaration",
        has=Relation(
            field="interfaces",
            has=Relation(
                stopBy="end",
                kind="type_identifier",
                regex="^" + RPC_COMMAND_IFACE_NAME + "$",
            ),
        ),
    )
    if not class_decl:
        return

    name_decl = class_decl.find(
        kind="method_declaration",
        pattern='@Override public String getName() { return "$NAME"; }',
    )
    if not name_decl:
        print(f"Skipping {root.get_root().filename} due to no getName() decl", file=sys.stderr)
        return
    else:
        name = name_decl["NAME"].text()
        name = name[0].upper() + name[1:]  # camelCase -> PascalCase

        print()
        print("@dataclass(frozen=True, kw_only=True)")
        print(f"class {name}(RpcCommand):")

    subp_decl = class_decl.find(
        kind="method_declaration",
        pattern="@Override public void attachToSubparser($$$) { $$$BODY }",
    )
    if not subp_decl:
        print(
            f"Skipping {root.get_root().filename} due to no attachToSubparser() decl",
            file=sys.stderr,
        )
        return

    subp_body_stmts = subp_decl.get_multiple_matches("BODY")

    # save for later use
    if cmd_help_decl := subp_decl.find(pattern='subparser.help("$HELP");'):
        subp_body_stmts.remove(cmd_help_decl)
    else:
        cmd_help_decl = None

    args = list[ArgInfo]()
    mutex_argses = dict[str, list[ArgInfo]]()
    mutex_required = dict[str, bool]()
    for stmt in subp_body_stmts:
        if add_arg_call := stmt.find(pattern="$OBJ.addArgument($$$)"):
            arg = get_arg_decl(add_arg_call)
            if arg.name not in EXCLUDED_ARGS[name]:
                args.append(arg)
                if (mutex := arg.arg_container) != "subparser":
                    mutex_argses[arg.arg_container].append(arg)
        elif mutex_decl := stmt.find(pattern="subparser.addMutuallyExclusiveGroup()"):
            assert stmt.kind() == "local_variable_declaration"
            mutex = val(val(stmt.field("declarator")).field("name")).text()
            required = val(mutex_decl.parent()).matches(pattern="$_.required(true)")
            mutex_argses[mutex] = []
            mutex_required[mutex] = required
            assert mutex_decl.ancestors()[int(required)].kind() == "variable_declarator"
        else:
            print(
                f"Warning: Unhandled statement from attachToSubparser(...): {stmt.text()}",
                file=sys.stderr,
            )

    if mutex_argses:
        # check if EXCLUDED_ARGS reduced a mutex down to one option
        for arg in (
            arg
            for mutex, mutex_args in mutex_argses.items()
            for arg in mutex_args
            if len(mutex_args) == 1 and mutex_required[mutex]
        ):
            arg.optional = False

    # declare fields without defaults first
    args.sort(key=ArgInfo.python_sort)

    if cmd_help_decl:
        cmd_help = rewrap(cmd_help_decl["HELP"].text())
        args_help = (
            "\n".join(
                rewrap(f":param {arg.name}: {arg.doc_text}", subsequent_indent="    ")
                for arg in args
            )
            if args
            else None
        )
        cmd_docstring = format_docstring("\n\n".join(filter(None, [cmd_help, args_help])))
        print(indent(cmd_docstring, "    "))
        print()

    for arg in args:
        print(indent(arg.render(), "    "))

    print()

    if mutex_argses:
        # figure out if we want overloaded __init__ methods
        arg_groups = groupby(args, lambda arg: arg.arg_container)
        arg_group_options = [
            (
                # include "nothing from this group" as an option if mutex group is optional
                ([[]] if not mutex_required[arg_container] else [])
                +
                # include each arg on its own, in required form for its solo overload
                [
                    [
                        replace(
                            arg,
                            optional=False,
                            type_expr="Literal[True]" if arg.type_expr == "bool" else arg.type_expr,
                            default_expr=None if arg.type_expr == "bool" else arg.default_expr,
                        )
                    ]
                    for arg in args_in_group
                ]
            )
            if len(mutex_argses.get(arg_container, [])) > 1
            # all args are a bundle (1 option)
            else ([args_in_group])
            for arg_container, _args_exhaustible in arg_groups
            if (args_in_group := list(_args_exhaustible))
        ]
        args_options = [list(chain(*argses)) for argses in product(*arg_group_options)]

        if len(args_options) > 1:
            # define __init__ overloads
            for args_option in args_options:
                print()
                print("    @overload")
                print("    def __init__(self, *, ", end="")
                args_option.sort(key=ArgInfo.python_sort)
                print(
                    ", ".join(replace(arg, doc_text=None).render() for arg in args_option), end=""
                )
                print("): ...")

            # define __init__ implementation
            print()
            print("    def __init__(self, **kwargs):")
            init = ""
            init += "self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})\n"
            init += "self.__dict__.update(kwargs)\n"
            for mutex, required in mutex_argses.items():
                mutex_argnames_str = ", ".join(
                    repr(arg.name) for arg in args if arg.arg_container == mutex
                )
                init += f"match len(kwargs.keys() & (args := {{{mutex_argnames_str}}})):\n"
                if required:
                    init += "    case 0:\n"
                    init += '        raise ValueError(f"One of {args} is required!")\n'
                    init += "    case 1:\n"
                    init += "        pass\n"
                else:
                    init += "    case 0 | 1:\n"
                    init += "        pass\n"
                init += "    case _:\n"
                init += '        raise ValueError(f"Arguments {args} are mutually exclusive!")\n'

            print(indent(init, " " * 8))
            print()

    if not cmd_help_decl and not args:
        print("    pass")
        print()


@dataclass
class ArgInfo:
    arg_container: str
    name: str
    doc_text: str | None = None
    type_expr: str = "str"  # default CLI arg type if none overridden
    optional: bool = True
    default_expr: str | None = None

    def render(self):
        return "".join(
            [
                self.name,
                ": ",
                f"Optional[{self.type_expr}]" if self.optional else self.type_expr,
                (
                    f" = {default}"
                    if (default := self.default_expr or ("None" if self.optional else None))
                    else ""
                ),
                f"\n{format_docstring(rewrap(self.doc_text))}" if self.doc_text else "",
            ]
        )

    def python_sort(self):
        "sort key to move args without defaults to the front"
        return self.default_expr is not None


def get_arg_decl(add_arg_call: SgNode) -> ArgInfo:
    assert (_opt_args := add_arg_call.field("arguments"))
    assert (_opt_tok := _opt_args.find(pattern='"$OPT"', regex='^"(--|[^-])'))
    first_long_opt = _opt_tok["OPT"].text()
    arg_name_snake = first_long_opt.lstrip("-").replace("-", "_")

    addl_arg_calls: dict[str, str] = {
        val(chained_call.field("name")).text(): (
            val(chained_call.field("arguments")).text()[1:-1].strip()
        )
        for chained_call in takewhile(
            lambda n: n.kind() == "method_invocation", add_arg_call.ancestors()
        )
    }

    container = add_arg_call["OBJ"].text()
    arg = ArgInfo(container, arg_name_snake)

    while addl_arg_calls:
        match addl_arg_calls:
            case {"help": doc_expr, **rest}:
                arg.doc_text = " ".join(doc_expr.strip().split()).replace('" + "', "").strip('"')
                addl_arg_calls = rest
            case {"action": "Arguments.storeTrue()", **rest}:
                arg.type_expr = "bool"
                arg.optional = False
                arg.default_expr = "False"
                addl_arg_calls = rest
            case {"choices": choices, **rest}:
                arg.type_expr = f"Literal[{choices}]"
                addl_arg_calls = rest
            case {"type": type, **rest}:
                arg.type_expr = {
                    "int": "int",
                    "long": "int",
                    "Boolean": "bool",
                    "Arguments.enumStringType(MessageRequestResponseType.class)": 'Literal["accept", "delete"]',
                }[type.removesuffix(".class")]
                addl_arg_calls = rest
            case {"nargs": '"*"', **rest}:
                arg.name += "s"
                arg.type_expr = f"tuple[{arg.type_expr}, ...]"
                arg.default_expr = "()"
                arg.optional = False
                addl_arg_calls = rest
            case {"nargs": '"+"', **rest}:
                arg.name += "s"
                arg.type_expr = f"NonEmptyTuple[{arg.type_expr}]"
                addl_arg_calls = rest
            case {"required": "true", **rest}:
                arg.optional = False
                addl_arg_calls = rest
            case _:
                raise ValueError(f"Don't know how to handle arg calls: {addl_arg_calls}")

    return arg


if __name__ == "__main__":
    gen()
