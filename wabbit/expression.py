import dataclasses
import enum


class Expr:
    pass


class TypeEnum(enum.Enum):
    BOOL = "bool"
    FLOAT = "float"
    INT = "int"


class OperatorEnum(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    EQ = "="
    EQ_EQ = "=="
    LESS = "<"
    LESS_EQ = "<="
    GREAT = ">"
    GREAT_EQ = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"


# Primitives


@dataclasses.dataclass
class Boolean(Expr):
    value: str


@dataclasses.dataclass
class Float(Expr):
    value: str


@dataclasses.dataclass
class Integer(Expr):
    value: str


# Names


@dataclasses.dataclass
class Name(Expr):
    text: str


@dataclasses.dataclass
class Type(Expr):
    type_enum: TypeEnum


# Expressions


@dataclasses.dataclass
class Assign(Expr):
    name: Name
    value: Expr


@dataclasses.dataclass
class Binary(Expr):
    left: Expr
    operator: OperatorEnum
    right: Expr


@dataclasses.dataclass
class Grouping(Expr):
    expression: Expr


@dataclasses.dataclass
class Unary(Expr):
    operator: OperatorEnum
    right: Expr
