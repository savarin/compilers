from typing import Optional
import dataclasses
import enum

import expression


class DeclarationType(enum.Enum):
    CONST = "CONST"
    VAR = "VAR"


class Statement:
    pass


# Statements


@dataclasses.dataclass
class Declaration(Statement):
    name: expression.Name
    declaration_type: DeclarationType
    value_type: Optional[expression.Type]
    initializer: Optional[expression.Expression]


@dataclasses.dataclass
class Print(Statement):
    expression: expression.Expression
