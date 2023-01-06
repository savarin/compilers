import abc


class Node:
    pass


class Assign(Node):
    def __init__(self, expression, value):
        self.expression = expression
        self.value = value


class Binary(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Constant(Node):
    def __init__(self, expression):
        self.expression = expression


class Grouping(Node):
    def __init__(self, expression):
        self.expression = expression


class Literal(Node):
    def __init__(self, value):
        self.value = value


class Name(Node):
    def __init__(self, name):
        self.name = name


class Print(Node):
    def __init__(self, value):
        self.value = value


class Type(Node):
    def __init__(self, expression, type_class):
        self.expression = expression
        self.type = type_class


class Unary(Node):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Variable(Node):
    def __init__(self, expression):
        self.expression = expression
