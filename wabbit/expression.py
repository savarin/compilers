import dataclasses


class Expr:
    pass


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
    text: str


# Expressions


@dataclasses.dataclass
class Assign(Expr):
    name: Name
    value: Expr


@dataclasses.dataclass
class Binary(Expr):
    left: Expr
    operator: str
    right: Expr


@dataclasses.dataclass
class Grouping(Expr):
    expression: Expr


@dataclasses.dataclass
class Unary(Expr):
    operator: str
    right: Expr
