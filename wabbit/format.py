from model import *


def format(node: Node) -> str:
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
            constant_type = f" {format(constant_type)}" if constant_type else ""
            return f"const {format(name)}{constant_type} = {format(initializer)};\n"

        case VariableDeclaration(name, variable_type, initializer):
            variable_type = f" {format(variable_type)}" if variable_type else ""
            initializer = f" = {format(initializer)}" if initializer else ""

            return f"var {format(name)}{variable_type}{initializer};\n"

        case _:
            raise Exception("Exhaustive switch error.")
