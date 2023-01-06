from typing import Optional
from dataclasses import dataclass


class Node:
    pass


class Expression(Node):
    pass


class Statement(Node):
    pass


# Types


@dataclass
class Integer(Expression):
    value: str


@dataclass
class Float(Expression):
    value: str


# Expressions


@dataclass
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class Grouping(Expression):
    expression: Expression


# Statements


@dataclass
class Print(Statement):
    expression: Expression


@dataclass
class Name(Expression):
    text: str


@dataclass
class Unary(Expression):
    operator: str
    right: Expression
