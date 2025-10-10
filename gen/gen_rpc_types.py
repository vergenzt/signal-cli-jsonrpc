from ast import AnnAssign, Constant, Name, Subscript, expr, unparse
from pathlib import Path

from ast_grep_py import Relation, Rule, SgNode, SgRoot

from .utils import val


JAVA_JSON_TYPE_FILES = sorted(
    Path(__file__).parent.glob("../signal-cli/src/main/java/org/asamk/signal/json/*.java")
)


def gen():
    print("from dataclasses import MISSING, dataclass, fields")
    print("from typing import Literal, Optional, overload")
    print()
    print()

    for file in JAVA_JSON_TYPE_FILES:
        process_file(SgRoot(file.read_text(), "java").root())


def process_file(root: SgNode):
    rec_decl = root.find(
        kind="record_declaration",
        all=[
            Rule(has=Relation(field="name", pattern="$NAME", regex="^Json")),
            Rule(has=Relation(field="parameters", pattern="$RECORD_FIELDS")),
            Rule(has=Relation(field="body", pattern="$BODY")),
        ],
    )
    if not rec_decl:
        return

    name = val(rec_decl["NAME"]).text().removeprefix("Json")
    params = [transform_param(p) for p in val(rec_decl["RECORD_FIELDS"]).children()]


def transform_param(formal_param: SgNode) -> AnnAssign:
    java_name = val(formal_param.field("name")).text()
    java_type_node = val(formal_param.field("type"))

    if formal_param.has(kind="modifiers") and val(formal_param.child(0)).text() == "@JsonInclude(JsonInclude.Include.NON_NULL)":
        py_default_node = Constant(None)
    else:
        py_default_node = None

    py_name = java_name.removeprefix("Json")
    py_type_node = transform_type(java_type_node)
    return AnnAssign(target=Name(id=py_name), annotation=py_type_node, value=py_default_node, simple=1)


def transform_type(java_type_node: SgNode) -> expr:
    if java_type_node.text() == "byte[]":
        return Name("bytes")

    match java_type_node.kind(), java_type_node.text():
        case "type_identifier", java_type:
            py_type = Name(next(v for k, v in {
                ("String",): "str",
                ("int", "long", "Integer", "Long"): "int",
                ("Float",): "float",
                ("boolean", "Boolean"): "bool",
            }.items() if java_type in k))
            return py_type if java_type[0].islower() else Subscript(Name("Optional"), py_type)

        case "generic_type", _:
            


# - { id: bytes, rule: { pattern: 'byte[]' }, fix: bytes }
# - { id: ints-or-longs, rule: { regex: '^(int|long)$' }, fix: int }
# - { id: ints-or-longs-nullable, rule: { regex: '^(Integer|Long)$' }, fix: 'Optional[int]' }
# - { id: float, rule: { regex: '^Float$' }, fix: float }
# - { id: boolean, rule: { regex: '^([Bb]oolean)$' }, fix: bool }

# - id: list-or-set
#   rule:
#     any:
#     - pattern: List<$TYPE>
#     - pattern: Set<$TYPE>
#   transform: *rewrite-type
#   fix: 'list[$PY_TYPE]'

# - id: optional
#   rule:
#     pattern: Optional<$TYPE>
#   transform: *rewrite-type
#   fix: '$PY_TYPE | None'


    return AnnAssign(
        Name(id=java_name.removeprefix("Json")),
        Name(id=

    )

#     kind: formal_parameter
#     all:
#     - has: { field: type, pattern: $TYPE }
#     - has: { field: name, pattern: $NAME }
#     - any:
#       - has: { stopBy: end, kind: annotation, regex: '^@JsonInclude\(JsonInclude\.Include\.NON_NULL\)$', pattern: $OPTIONAL }
#       - pattern: $_


# - id: record
#   rule:
#     kind: record_declaration
#     all:
#     - has: { field: name, pattern: $TYPE }
#     - has: { field: parameters, pattern: $RECORD_FIELDS }
#     - has: { field: body, pattern: $BODY }
#   transform:
#     PY_TYPE: &strip-leading-json
#       replace:
#         source: $TYPE
#         replace: '^Json'
#         by: ''
#     PY_RECORD_FIELDS:
#       rewrite:
#         source: $RECORD_FIELDS
#         rewriters: [record_field]
#         joinBy: "\n"
#     PY_BODY:
#       rewrite:
#         source: $BODY
#         rewriters: *prog-rewriters
#         joinBy: ""
#   fix: |-

#     @dataclass
#     class $PY_TYPE:
#         $PY_RECORD_FIELDS
#     $PY_BODY

# - id: record_field
#   rule:
#     kind: formal_parameter
#     all:
#     - has: { field: type, pattern: $TYPE }
#     - has: { field: name, pattern: $NAME }
#     - any:
#       - has: { stopBy: end, kind: annotation, regex: '^@JsonInclude\(JsonInclude\.Include\.NON_NULL\)$', pattern: $OPTIONAL }
#       - pattern: $_
#   fix: |-
#     $NAME: $PY_TYPE
#   transform: &rewrite-type
#     PY_TYPE:
#       rewrite:
#         source: $TYPE
#         rewriters:
#         - strip-leading-json
#         - string
#         - bytes
#         - ints-or-longs
#         - ints-or-longs-nullable
#         - float
#         - boolean
#         - list-or-set
#         - optional

# - id: strip-leading-json
#   rule: { regex: '^Json', pattern: '$TYPE' }
#   transform:
#     PY_TYPE: *strip-leading-json
#   fix: $PY_TYPE

# - { id: string, rule: { regex: '^String$' }, fix: 'Optional[str]' }
# - { id: bytes, rule: { pattern: 'byte[]' }, fix: bytes }
# - { id: ints-or-longs, rule: { regex: '^(int|long)$' }, fix: int }
# - { id: ints-or-longs-nullable, rule: { regex: '^(Integer|Long)$' }, fix: 'Optional[int]' }
# - { id: float, rule: { regex: '^Float$' }, fix: float }
# - { id: boolean, rule: { regex: '^([Bb]oolean)$' }, fix: bool }

# - id: list-or-set
#   rule:
#     any:
#     - pattern: List<$TYPE>
#     - pattern: Set<$TYPE>
#   transform: *rewrite-type
#   fix: 'list[$PY_TYPE]'

# - id: optional
#   rule:
#     pattern: Optional<$TYPE>
#   transform: *rewrite-type
#   fix: '$PY_TYPE | None'

# - id: enum
#   rule:
#     kind: enum_declaration
#     all:
#     - has: { field: name, pattern: $TYPE }
#     - has: { field: body, pattern: $BODY }
#   transform:
#     PY_TYPE: *strip-leading-json
#     PY_ENUM_MEMBERS:
#       rewrite:
#         source: $BODY
#         rewriters: [enum-member]
#         joinBy: "\n"
#   fix: |

#     class $PY_TYPE(StrEnum):
#         $PY_ENUM_MEMBERS

# - id: enum-member
#   rule:
#     kind: enum_constant
#     pattern: $MEMBER_NAME
#   fix: |-
#     $MEMBER_NAME = auto()

if __name__ == "__main__":
    main()
