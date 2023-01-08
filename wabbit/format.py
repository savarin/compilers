from typing import Union
from expression import *
from statement import *


def format(node: Union[Expression, Statement, None]) -> str:
    match node:
        case Boolean(value):
            return value

        case Float(value):
            return value

        case Integer(value):
            return value

        case Name(text):
            return text

        case TypeName(text):
            return text

        case Assign(name, value):
            return f"{format(name)} = {format(value)};\n"

        case Binary(left, operator, right):
            return f"{format(left)} {operator} {format(right)}"

        case Grouping(expression):
            return f"({format(expression)})"

        case Unary(operator, right):
            return f"{operator}{format(right)}"

        case Print(expression):
            return f"print {format(expression)};\n"

        case ConstantDeclaration(name, constant_type, initializer):
            type_string = (
                f" {format(constant_type)}" if constant_type is not None else ""
            )
            return f"const {format(name)}{type_string} = {format(initializer)};\n"

        case VariableDeclaration(name, variable_type, initializer):
            type_string = (
                f" {format(variable_type)}" if variable_type is not None else ""
            )
            init_string = f" = {format(initializer)}" if initializer else ""

            return f"var {format(name)}{type_string}{init_string};\n"

        case _:
            raise Exception("Exhaustive switch error.")
