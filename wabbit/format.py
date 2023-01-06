from model import *


def format(node: Node) -> str:
    if isinstance(node, Float):
        return node.value

    elif isinstance(node, Integer):
        return node.value

    elif isinstance(node, Name):
        return node.text

    elif isinstance(node, TypeName):
        return node.text

    elif isinstance(node, Assign):
        return f"{format(node.name)} = {format(node.value)};\n"

    elif isinstance(node, Binary):
        return f"{format(node.left)} {node.operator} {format(node.right)}"

    elif isinstance(node, Grouping):
        return f"({format(node.expression)})"

    elif isinstance(node, Unary):
        return f"{node.operator}{format(node.right)}"

    elif isinstance(node, Print):
        return f"print {format(node.expression)};\n"

    elif isinstance(node, ConstantDeclaration):
        constant_type = f" {format(node.constant_type)}" if node.constant_type else ""
        return (
            f"const {format(node.name)}{constant_type} = {format(node.initializer)};\n"
        )

    elif isinstance(node, VariableDeclaration):
        variable_type = f" {format(node.variable_type)}" if node.variable_type else ""
        initializer = f" = {format(node.initializer)}" if node.initializer else ""

        return f"var {format(node.name)}{variable_type}{initializer};\n"

    raise Exception("Exhaustive switch error.")
