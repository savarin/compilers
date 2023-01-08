from typing import Union
from expression import *
from statement import *


def format(node: Union[Expr, Statem, None]) -> str:
    match node:
        case Boolean(value):
            return value

        case Float(value):
            return value

        case Integer(value):
            return value

        case Name(text):
            return text

        case Type(type_enum):
            return type_enum.value

        case Assign(name, value):
            return f"{format(name)} = {format(value)}"

        case Binary(left, operator, right):
            return f"{format(left)} {operator.value} {format(right)}"

        case Grouping(expression):
            return f"({format(expression)})"

        case Unary(operator, right):
            return f"{operator.value}{format(right)}"

        case Block(statements):
            result = "{\n"

            for statement in statements:
                result += "    " + format(statement)

            return result + "}"

        case Declaration(name, declaration_type, value_type, initializer):
            declaration = declaration_type.value
            value = f" {format(value_type)}" if value_type is not None else ""
            init = f" = {format(initializer)}" if initializer else ""

            return f"{declaration} {format(name)}{value}{init};\n"

        case Expression(expression):
            return f"{format(expression)};\n"

        case If(condition, then_branch, else_branch):
            else_string = (
                f" else {format(else_branch)}" if else_branch is not None else ""
            )

            return f"if {format(condition)} {format(then_branch)}" + else_string

        case Print(expression):
            return f"print {format(expression)};\n"

        case While(condition, body):
            return f"while {format(condition)} {format(body)}"

        case _:
            raise Exception("Exhaustive switch error.")
