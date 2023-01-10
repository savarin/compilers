from typing import List
import dataclasses
import enum


class Expr:
    pass


class TypeEnum(enum.Enum):
    BOOL = "BOOL"
    FLOAT = "FLOAT"
    INT = "INT"


class OperatorEnum(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    EQUAL = "="
    EQUAL_EQUAL = "=="
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="
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


# Name / Type


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
class Call(Expr):
    callee: Expr
    arguments: List[Expr]


@dataclasses.dataclass
class Grouping(Expr):
    expression: Expr


@dataclasses.dataclass
class Unary(Expr):
    operator: OperatorEnum
    right: Expr
