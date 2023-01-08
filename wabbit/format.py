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

        case Call(callee, arguments):
            return f"{format(callee)}({', '.join([format(argument) for argument in arguments])})"

        case Grouping(expression):
            return f"({format(expression)})"

        case Unary(operator, right):
            return f"{operator.value}{format(right)}"

        case Block(statements):
            result = "{\n"

            for statement in statements:
                result += "    " + format(statement)

            return result + "}\n"

        case Break():
            return "break;\n"

        case Continue():
            return "continue;\n"

        case Declaration(name, declaration_type, value_type, initializer):
            declaration = declaration_type.value
            value = f" {format(value_type)}" if value_type is not None else ""
            init = f" = {format(initializer)}" if initializer else ""

            return f"{declaration} {format(name)}{value}{init};\n"

        case Expression(expression):
            return f"{format(expression)};\n"

        case Function(name, parameters, parameter_types, return_type, body):
            parameters_string = ", ".join(
                [
                    format(parameter) + " " + format(parameter_type)
                    for parameter, parameter_type in zip(parameters, parameter_types)
                ]
            )
            return f"func {format(name)}({parameters_string}) {format(return_type)} {format(body)}"

        case If(condition, then_branch, else_branch):
            if_then_string = f"if {format(condition)} {format(then_branch)}"

            if else_branch is not None:
                if_then_string = if_then_string.rstrip("\n")

            else_string = (
                f" else {format(else_branch)}" if else_branch is not None else ""
            )

            return if_then_string + else_string

        case Print(expression):
            return f"print {format(expression)};\n"

        case Return(expression):
            return f"return {format(expression)};\n"

        case While(condition, body):
            return f"while {format(condition)} {format(body)}"

        case _:
            raise Exception("Exhaustive switch error.")
