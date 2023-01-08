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

        case Type(text):
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

        case Declaration(name, declaration_type, value_type, initializer):
            declaration = declaration_type.value.lower()
            value = f" {format(value_type)}" if value_type is not None else ""
            init = f" = {format(initializer)}" if initializer else ""

            return f"{declaration} {format(name)}{value}{init};\n"

        case _:
            raise Exception("Exhaustive switch error.")
