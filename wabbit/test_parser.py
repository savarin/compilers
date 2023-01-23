from typing import List

from parser import init_parser, parse
from scanner import init_scanner, scan
from expression import TypeEnum, Integer, Name, Type
from statement import DeclarationEnum, Statem, Break, Continue, Print, Declaration


def source_to_statements(source: str) -> List[Statem]:
    tokens = scan(init_scanner(source))
    return parse(init_parser(tokens))


def test_parse():
    # program 1
    statements = source_to_statements("break;")
    assert isinstance(statements[0], Break)

    # program 2
    statements = source_to_statements("continue;")
    assert isinstance(statements[0], Continue)

    # program 3
    statements = source_to_statements("print 1;")
    assert isinstance(statements[0], Print)
    assert isinstance(statements[0].expression, Integer)
    assert statements[0].expression.value == "1"

    # program 4
    statements = source_to_statements(
        """\
print 1;
print 2;
print 3;
"""
    )

    assert isinstance(statements[0], Print)
    assert isinstance(statements[0].expression, Integer)
    assert statements[0].expression.value == "1"

    assert isinstance(statements[1], Print)
    assert isinstance(statements[1].expression, Integer)
    assert statements[1].expression.value == "2"

    assert isinstance(statements[2], Print)
    assert isinstance(statements[2].expression, Integer)
    assert statements[2].expression.value == "3"

    # program 5
    statements = source_to_statements(
        """\
const a = 1;
const a int = 1;
"""
    )

    assert isinstance(statements[0], Declaration)
    assert statements[0].name == Name("a")
    assert statements[0].declaration_enum == DeclarationEnum.CONST
    assert statements[0].value_type is None
    assert isinstance(statements[0].initializer, Integer)
    assert statements[0].initializer.value == "1"

    assert isinstance(statements[1], Declaration)
    assert statements[1].name == Name("a")
    assert statements[1].declaration_enum == DeclarationEnum.CONST
    assert statements[1].value_type == Type(TypeEnum.INT)
    assert isinstance(statements[1].initializer, Integer)
    assert statements[1].initializer.value == "1"

    # program 6
    statements = source_to_statements(
        """\
var x int = 1;
var x = 1;
var x int;
"""
    )

    assert isinstance(statements[0], Declaration)
    assert statements[0].name == Name("x")
    assert statements[0].declaration_enum == DeclarationEnum.VAR
    assert statements[0].value_type == Type(TypeEnum.INT)
    assert isinstance(statements[0].initializer, Integer)
    assert statements[0].initializer.value == "1"

    assert isinstance(statements[1], Declaration)
    assert statements[1].name == Name("x")
    assert statements[1].declaration_enum == DeclarationEnum.VAR
    assert statements[1].value_type is None
    assert isinstance(statements[1].initializer, Integer)
    assert statements[1].initializer.value == "1"

    assert isinstance(statements[2], Declaration)
    assert statements[2].name == Name("x")
    assert statements[2].declaration_enum == DeclarationEnum.VAR
    assert statements[2].value_type == Type(TypeEnum.INT)
    assert statements[2].initializer is None

    # program 7
    statements = source_to_statements(
        """\
if true { print 2; } else { print 3; }
if true { print 2; }
"""
    )

    assert str(statements[0]) == (
        "If(condition=Boolean(value='true'),"
        + " then_branch=Block(statements=[Print(expression=Integer(value='2'))]),"
        + " else_branch=Block(statements=[Print(expression=Integer(value='3'))]))"
    )
    assert str(statements[1]) == (
        "If(condition=Boolean(value='true'),"
        + " then_branch=Block(statements=[Print(expression=Integer(value='2'))]),"
        + " else_branch=None)"
    )

    # program 8
    statements = source_to_statements(
        """\
while true { print 2; }
"""
    )

    assert str(statements[0]) == (
        "While(condition=Boolean(value='true'),"
        + " body=Block(statements=[Print(expression=Integer(value='2'))]))"
    )
