import ast as a
from pathlib import Path
from subprocess import check_output as sh
from typing import cast

from ast_grep_py import SgNode, SgRoot
from caseutil import to_snake

from .utils import PyImports, py_dataclass_deco, val

JAVA_JSON_TYPE_FILES = sorted(
    Path(__file__).parent.glob("../signal-cli/src/main/java/org/asamk/signal/json/*.java")
)


def main():
    py_ast = gen()
    py_src = a.unparse(py_ast)
    py_src = sh(["ruff", "format", "-"], text=True, input=py_src)
    py_src = sh(["ruff", "check", "--quiet", "--select=I", "--fix", "-"], text=True, input=py_src)
    print(py_src)


def gen() -> a.Module:
    py_imports = PyImports()

    py_decls = [
        py_decl
        for file in JAVA_JSON_TYPE_FILES
        if (java_prog_n := SgRoot(file.read_text(), "java").root())
        for java_n in java_prog_n.children()
        if java_n.kind() not in ("package_declaration", "import_declaration")
        if (py_decl := get_py_decl(java_n, py_imports))
    ]

    py_import_decls = [
        a.ImportFrom(mod, [a.alias(n) for n in names], level=0) for mod, names in py_imports.items()
    ]

    py_body = list[a.stmt]()
    py_body.extend(py_import_decls)
    py_body.extend(py_decls)
    return a.Module(py_body)


def get_py_decl(java_decl_n: SgNode, py_imports: PyImports) -> a.ClassDef | None:
    py_type_decos = tuple[a.expr]()
    py_type_name = val(java_decl_n.field("name")).text().removeprefix("Json")
    py_bases = tuple[a.expr]()
    py_body = tuple[a.stmt]()

    match java_decl_n.kind():
        case "record_declaration":
            py_type_decos = (py_dataclass_deco(py_imports),)
            py_body = tuple(
                sorted(
                    [
                        get_py_param_decl(java_param, py_imports)
                        for java_param in filter(
                            SgNode.is_named, val(java_decl_n.field("parameters")).children()
                        )
                    ],
                    key=lambda ann_assign: cast(a.AnnAssign, ann_assign).target is not None,
                )
            )
            if java_decl_body := java_decl_n.field("body"):
                py_body = py_body + tuple(
                    py_decl
                    for decl in java_decl_body.children()
                    if decl.kind().removesuffix("_declaration") in ("record", "enum")
                    if (py_decl := get_py_decl(decl, py_imports))
                )

        case "enum_declaration":
            py_type_decos = ()
            py_bases = (py_imports.add("enum", "StrEnum"),)
            py_body = tuple(
                a.Assign(
                    [a.Name(val(enum_member.field("name")).text())],
                    a.Call(py_imports.add("enum", "auto"), []),
                    lineno=0,
                )
                for enum_member in val(java_decl_n.field("body")).children()
                if enum_member.kind() == "enum_constant"
            )

        case "class_declaration":
            pass

        case _:
            raise NotImplementedError(
                f"Unhandled declaration type `{java_decl_n.kind()}`: {java_decl_n.text()}"
            )

    return (
        a.ClassDef(
            decorator_list=list(py_type_decos),
            name=py_type_name,
            bases=list(py_bases),
            body=list(py_body),
        )
        if py_body
        else None
    )


def get_py_param_decl(java_param: SgNode, py_imports: PyImports) -> a.AnnAssign:
    java_param_name = val(java_param.field("name")).text()
    java_param_type_node = val(java_param.field("type"))

    py_param_name = to_snake(java_param_name)
    py_param_type_node = get_py_type(java_param_type_node, py_imports)
    py_assign_tgt: a.expr | None = None

    if (
        next(filter(SgNode.is_named, java_param.children())).text()
        == "@JsonInclude(JsonInclude.Include.NON_NULL)"
    ):
        # include a falsy default if field might be omitted
        match py_param_type_node:
            case a.BinOp(_, a.BitOr(), a.Constant(None)):
                py_assign_tgt = a.Constant(None)
            case a.Subscript(a.Name("tuple"), _):
                py_assign_tgt = a.Tuple([])

    return a.AnnAssign(
        target=a.Name(id=py_param_name),
        annotation=py_param_type_node,
        value=py_assign_tgt,
        simple=1,
    )


def get_py_type(java_type_n: SgNode, py_imports: PyImports) -> a.expr:
    java_type_s = java_type_n.text()
    if java_type_s == "byte[]":
        return a.Name("bytes")

    elif java_type_n.kind() == "generic_type":
        java_gentype_n, java_type_params = java_type_n.children()
        [java_gentypeparam_n] = filter(SgNode.is_named, java_type_params.children())
        match java_gentype_s := java_gentype_n.text():
            case "Optional":
                # Java `Optional` type params are always objects, and can always be nullable
                # -> result is same type as the type param
                return get_py_type(java_gentypeparam_n, py_imports)
            case "List":
                return a.Subscript(
                    a.Name("tuple"),
                    a.Tuple([get_py_type(java_gentypeparam_n, py_imports), a.Constant(...)]),
                )
            case _:
                raise NotImplementedError(f"Unhandled Java generic type: {java_gentype_s}")

    else:
        match java_type_s:
            case "String":
                py_type_n = a.Name("str")
            case "int" | "long" | "Integer" | "Long":
                py_type_n = a.Name("int")
            case "Float":
                py_type_n = a.Name("float")
            case "boolean" | "Boolean":
                py_type_n = a.Name("bool")
            case _ if java_type_n.kind() == "type_identifier":
                # assume an unknown identifier is another type we're defining
                py_type_n = a.Name(java_type_s.removeprefix("Json"))
            case _:
                raise NotImplementedError(
                    f"Unhandled Java type of kind {java_type_n.kind()}: {java_type_s}"
                )

        # java types beginning with a capital letter are object types and may be null
        if java_type_s[0].isupper():
            return a.BinOp(py_type_n, a.BitOr(), a.Constant(None))
        else:
            return py_type_n


if __name__ == "__main__":
    main()
