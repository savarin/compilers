import model


def format(node: model.Node) -> str:
    if isinstance(node, model.Assign):
        return f"{format(node.expression)} = {format(node.value)};\n"

    if isinstance(node, model.Binary):
        return f"{format(node.left)} {node.operator} {format(node.right)}"

    elif isinstance(node, model.Constant):
        return f"const {format(node.expression)}"

    elif isinstance(node, model.Grouping):
        return f"({format(node.expression)})"

    elif isinstance(node, model.Literal):
        return str(node.value)

    elif isinstance(node, model.Name):
        return node.name

    elif isinstance(node, model.Print):
        return f"print {format(node.value)};\n"

    elif isinstance(node, model.Type):
        return f"{format(node.expression)} {node.type};\n"

    elif isinstance(node, model.Unary):
        return f"{node.operator}{format(node.right)}"

    elif isinstance(node, model.Variable):
        return f"var {format(node.expression)}"

    raise Exception("Exhaustive switch error.")
