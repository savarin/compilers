from model import *


def format(node: Node) -> str:
    if isinstance(node, Float):
        return str(node.value)

    elif isinstance(node, Integer):
        return str(node.value)

    elif isinstance(node, Binary):
        return f"{format(node.left)} {node.operator} {format(node.right)}"

    elif isinstance(node, Grouping):
        return f"({format(node.expression)})"

    elif isinstance(node, Unary):
        return f"{node.operator}{format(node.right)}"

    elif isinstance(node, Print):
        return f"print {format(node.expression)};\n"

    raise Exception("Exhaustive switch error.")
