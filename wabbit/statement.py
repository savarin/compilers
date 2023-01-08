from typing import Optional
import dataclasses

import expression


class Statement:
    pass


# Statements


@dataclasses.dataclass
class Print(Statement):
    expression: expression.Expression


# Declarations


@dataclasses.dataclass
class ConstantDeclaration(Statement):
    name: expression.Name
    constant_type: Optional[expression.TypeName]
    initializer: expression.Expression


@dataclasses.dataclass
class VariableDeclaration(Statement):
    name: expression.Name
    variable_type: Optional[expression.TypeName]
    initializer: Optional[expression.Expression]
