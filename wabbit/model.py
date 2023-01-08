from typing import Optional
from dataclasses import dataclass


class Node:
    pass


class Expression(Node):
    pass


class Statement(Node):
    pass


class Declaration(Node):
    pass


class Type(Node):
    pass


# Primitives

@dataclass
class Boolean(Expression):
    value: str


@dataclass
class Float(Expression):
    value: str


@dataclass
class Integer(Expression):
    value: str


# Names


@dataclass
class Name(Expression):
    text: str


@dataclass
class TypeName(Expression):
    text: str


# Expressions


@dataclass
class Assign(Expression):
    name: Name
    value: Expression


@dataclass
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class Grouping(Expression):
    expression: Expression


@dataclass
class Unary(Expression):
    operator: str
    right: Expression


# Statements


@dataclass
class Print(Statement):
    expression: Expression


# Declarations


@dataclass
class ConstantDeclaration(Statement):
    name: Name
    constant_type: Optional[TypeName]
    initializer: Expression


@dataclass
class VariableDeclaration(Statement):
    name: Name
    variable_type: Optional[TypeName]
    initializer: Optional[Expression]
