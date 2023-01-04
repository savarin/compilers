import model


def format(node: model.Node) -> str:
    if isinstance(node, model.Binary):
        return f"{format(node.left)} {node.operator} {format(node.right)}"

    elif isinstance(node, model.Grouping):
        return f"({node.expression})"

    elif isinstance(node, model.Literal):
        return str(node.value)

    elif isinstance(node, model.Print):
        return f"print {format(node.value)};\n"

    elif isinstance(node, model.Unary):
        return f"{node.operator}{format(node.right)}"

    elif isinstance(node, model.Variable):
        return node.name

    raise Exception("Exhaustive switch error.")
