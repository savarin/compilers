from typing import List, Optional
import dataclasses
import enum

import expression


class DeclarationEnum(enum.Enum):
    CONST = "const"
    VAR = "var"


class Statem:
    pass


# Statements


@dataclasses.dataclass
class Block(Statem):
    statements: List[Statem]


@dataclasses.dataclass
class Declaration(Statem):
    name: expression.Name
    declaration_enum: DeclarationEnum
    value_type: Optional[expression.Type]
    initializer: Optional[expression.Expr]


@dataclasses.dataclass
class Expression(Statem):
    expression: expression.Expr


@dataclasses.dataclass
class If(Statem):
    condition: expression.Expr
    then_branch: Statem
    else_branch: Optional[Statem]


@dataclasses.dataclass
class Print(Statem):
    expression: expression.Expr


@dataclasses.dataclass
class While(Statem):
    condition: expression.Expr
    body: Statem
