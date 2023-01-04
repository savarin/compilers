import abc


class Node:
    pass


class Binary(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Node):
    def __init__(self, expression):
        self.expression = expression


class Literal(Node):
    def __init__(self, value):
        self.value = value


class Print(Node):
    def __init__(self, value):
        self.value = value


class Unary(Node):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Variable(Node):
    def __init__(self, name):
        self.name = name
