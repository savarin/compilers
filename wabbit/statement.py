from typing import Optional
import dataclasses
import enum

import expression


class DeclarationType(enum.Enum):
    CONST = "CONST"
    VAR = "VAR"


class Statem:
    pass


# Statements


@dataclasses.dataclass
class Declaration(Statem):
    name: expression.Name
    declaration_type: DeclarationType
    value_type: Optional[expression.Type]
    initializer: Optional[expression.Expr]


@dataclasses.dataclass
class Expression(Statem):
    expression: expression.Expr


@dataclasses.dataclass
class Print(Statem):
    expression: expression.Expr
