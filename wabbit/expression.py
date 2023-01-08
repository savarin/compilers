import dataclasses


class Expression:
    pass


# Primitives


@dataclasses.dataclass
class Boolean(Expression):
    value: str


@dataclasses.dataclass
class Float(Expression):
    value: str


@dataclasses.dataclass
class Integer(Expression):
    value: str


# Names


@dataclasses.dataclass
class Name(Expression):
    text: str


@dataclasses.dataclass
class Type(Expression):
    text: str


# Expressions


@dataclasses.dataclass
class Assign(Expression):
    name: Name
    value: Expression


@dataclasses.dataclass
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclasses.dataclass
class Grouping(Expression):
    expression: Expression


@dataclasses.dataclass
class Unary(Expression):
    operator: str
    right: Expression
