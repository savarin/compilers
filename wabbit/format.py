from typing import Union

from expression import (
    Expr,
    Boolean,
    Float,
    Integer,
    Name,
    Type,
    Assign,
    Binary,
    Call,
    Grouping,
    Unary,
)
from statement import (
    Statem,
    Block,
    Break,
    Continue,
    Declaration,
    Expression,
    Function,
    If,
    Print,
    Return,
    While,
)


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
            return type_enum.value.lower()

        case Assign(name, value):
            return f"{format(name)} = {format(value)}"

        case Binary(left, operator_enum, right):
            return f"{format(left)} {operator_enum.value} {format(right)}"

        case Call(callee, arguments):
            return f"{format(callee)}({', '.join([format(argument) for argument in arguments])})"

        case Grouping(expression):
            return f"({format(expression)})"

        case Unary(operator_enum, right):
            return f"{operator_enum.value}{format(right)}"

        case Block(statements):
            result = "{\n    "

            for statement in statements:
                result += format(statement).replace("\n", "\n    ")

            return result.rstrip("    ") + "}\n"

        case Break():
            return "break;\n"

        case Continue():
            return "continue;\n"

        case Declaration(name, declaration_type, value_type, initializer):
            value = f" {format(value_type)}" if value_type is not None else ""
            initial = f" = {format(initializer)}" if initializer is not None else ""

            return f"{declaration_type.value.lower()} {format(name)}{value}{initial};\n"

        case Expression(expression):
            return f"{format(expression)};\n"

        case Function(name, parameter_names, parameter_types, return_type, body):
            parameters = ", ".join(
                [
                    f"{format(parameter_name)} {format(parameter_type)}"
                    for parameter_name, parameter_type in zip(
                        parameter_names, parameter_types
                    )
                ]
            )
            return f"func {format(name)}({parameters}) {format(return_type)} {format(body)}"

        case If(condition, then_branch, else_branch):
            consequent = f"if {format(condition)} {format(then_branch)}"
            alternate = (
                f" else {format(else_branch)}" if else_branch is not None else ""
            )

            if else_branch is not None:
                consequent = consequent.rstrip("\n")

            return consequent + alternate

        case Print(expression):
            return f"print {format(expression)};\n"

        case Return(expression):
            return f"return {format(expression)};\n"

        case While(condition, body):
            return f"while {format(condition)} {format(body)}"

        case _:
            raise Exception("Exhaustive switch error.")
