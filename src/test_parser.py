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

    # program 9
    statements = source_to_statements("1;")

    assert str(statements[0]) == "Expression(expression=Integer(value='1'))"

    # program 10
    statements = source_to_statements(
        """\
print 1;
print 1.5;
print true;
print false;
print x;
"""
    )

    assert str(statements[0]) == "Print(expression=Integer(value='1'))"
    assert str(statements[1]) == "Print(expression=Float(value='1.5'))"
    assert str(statements[2]) == "Print(expression=Boolean(value='true'))"
    assert str(statements[3]) == "Print(expression=Boolean(value='false'))"
    assert str(statements[4]) == "Print(expression=Name(text='x'))"

    # program 11
    statements = source_to_statements(
        """\
print 1*2;
print x*y;
print 1/2;
print x/y;
print 1*2*3/x*y;
"""
    )

    assert str(statements[0]) == (
        "Print(expression=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='2')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Binary(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>, right=Name(text='y')))"
    )
    assert str(statements[2]) == (
        "Print(expression=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.DIVIDE: '/'>, right=Integer(value='2')))"
    )
    assert str(statements[3]) == (
        "Print(expression=Binary(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.DIVIDE: '/'>, right=Name(text='y')))"
    )
    assert str(statements[4]) == (
        "Print(expression=Binary(left=Binary(left=Binary(left=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='2')),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='3')),"
        + " operator_enum=<OperatorEnum.DIVIDE: '/'>,"
        + " right=Name(text='x')),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Name(text='y')))"
    )

    # program 12
    statements = source_to_statements(
        """\
print -2;
print +3;
print -x*y;
print x*-y;
"""
    )

    assert str(statements[0]) == (
        "Print(expression=Unary(operator_enum=<OperatorEnum.MINUS: '-'>,"
        + " right=Integer(value='2')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Unary(operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='3')))"
    )
    assert str(statements[2]) == (
        "Print(expression=Binary(left=Unary(operator_enum=<OperatorEnum.MINUS: '-'>,"
        + " right=Name(text='x')),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Name(text='y')))"
    )
    assert str(statements[3]) == (
        "Print(expression=Binary(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Unary(operator_enum=<OperatorEnum.MINUS: '-'>,"
        + " right=Name(text='y'))))"
    )

    # program 13
    statements = source_to_statements(
        """\
print 1 + 2;
print 3 - 4;
print a*b + c*d;
print 3 + 4*5;
print 3*4 + 5;
    """
    )

    assert str(statements[0]) == (
        "Print(expression=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='2')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.MINUS: '-'>,"
        + " right=Integer(value='4')))"
    )
    assert str(statements[2]) == (
        "Print(expression=Binary(left=Binary(left=Name(text='a'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Name(text='b')),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Binary(left=Name(text='c'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Name(text='d'))))"
    )
    assert str(statements[3]) == (
        "Print(expression=Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Binary(left=Integer(value='4'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='5'))))"
    )
    assert str(statements[4]) == (
        "Print(expression=Binary(left=Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='4')),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='5')))"
    )

    # program 14
    statements = source_to_statements(
        """\
print 2 <= 3;
print 2 > 3;
print 2 >= 3;
print 2 == 3;
print 2 != 3;
print a+b*c < d-e/f;
    """
    )

    assert str(statements[0]) == (
        "Print(expression=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.LESS_EQUAL: '<='>,"
        + " right=Integer(value='3')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.GREATER: '>'>,"
        + " right=Integer(value='3')))"
    )
    assert str(statements[2]) == (
        "Print(expression=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.GREATER_EQUAL: '>='>,"
        + " right=Integer(value='3')))"
    )

    assert str(statements[3]) == (
        "Print(expression=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.EQUAL_EQUAL: '=='>,"
        + " right=Integer(value='3')))"
    )
    assert str(statements[4]) == (
        "Print(expression=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.BANG_EQUAL: '!='>,"
        + " right=Integer(value='3')))"
    )
    assert str(statements[5]) == (
        "Print(expression=Binary(left=Binary(left=Name(text='a'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Binary(left=Name(text='b'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Name(text='c'))),"
        + " operator_enum=<OperatorEnum.LESS: '<'>,"
        + " right=Binary(left=Name(text='d'),"
        + " operator_enum=<OperatorEnum.MINUS: '-'>,"
        + " right=Binary(left=Name(text='e'),"
        + " operator_enum=<OperatorEnum.DIVIDE: '/'>,"
        + " right=Name(text='f')))))"
    )

    # program 15
    statements = source_to_statements(
        """\
print x && y;
print a < b && c > d;
    """
    )

    assert str(statements[0]) == (
        "Print(expression=Logical(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.AND: '&&'>,"
        + " right=Name(text='y')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Logical(left=Binary(left=Name(text='a'),"
        + " operator_enum=<OperatorEnum.LESS: '<'>,"
        + " right=Name(text='b')),"
        + " operator_enum=<OperatorEnum.AND: '&&'>,"
        + " right=Binary(left=Name(text='c'),"
        + " operator_enum=<OperatorEnum.GREATER: '>'>,"
        + " right=Name(text='d'))))"
    )

    # program 16
    statements = source_to_statements(
        """\
print x || y;
print a && b || c && d;
    """
    )

    assert str(statements[0]) == (
        "Print(expression=Logical(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.OR: '||'>,"
        + " right=Name(text='y')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Logical(left=Logical(left=Name(text='a'),"
        + " operator_enum=<OperatorEnum.AND: '&&'>,"
        + " right=Name(text='b')),"
        + " operator_enum=<OperatorEnum.OR: '||'>,"
        + " right=Logical(left=Name(text='c'),"
        + " operator_enum=<OperatorEnum.AND: '&&'>,"
        + " right=Name(text='d'))))"
    )

    # program 17
    statements = source_to_statements(
        """\
print (1+2)*(3+4);
print (1+2*(3+4))*5;
    """
    )

    assert str(statements[0]) == (
        "Print(expression=Binary(left=Grouping(expression=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='2'))),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Grouping(expression=Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='4')))))"
    )
    assert str(statements[1]) == (
        "Print(expression=Binary(left=Grouping(expression=Binary(left=Integer(value='1'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Binary(left=Integer(value='2'),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Grouping(expression=Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='4')))))),"
        + " operator_enum=<OperatorEnum.TIMES: '*'>,"
        + " right=Integer(value='5')))"
    )

    # program 18
    statements = source_to_statements(
        """\
x = 1;
print x = 1;
while (n = n + 1) < 10 {
   print n;
}
x = y = 2;
    """
    )

    assert str(statements[0]) == (
        "Expression(expression=Assign(name=Name(text='x'),"
        + " value=Integer(value='1')))"
    )
    assert str(statements[1]) == (
        "Print(expression=Assign(name=Name(text='x')," + " value=Integer(value='1')))"
    )
    assert str(statements[2]) == (
        "While(condition=Binary(left=Grouping(expression=Assign(name=Name(text='n'),"
        + " value=Binary(left=Name(text='n'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='1')))),"
        + " operator_enum=<OperatorEnum.LESS: '<'>,"
        + " right=Integer(value='10')),"
        + " body=Block(statements=[Print(expression=Name(text='n'))]))"
    )
    assert str(statements[3]) == (
        "Expression(expression=Assign(name=Name(text='x'),"
        + " value=Assign(name=Name(text='y'),"
        + " value=Integer(value='2'))))"
    )

    # program 19
    statements = source_to_statements(
        """\
func add(x int, y int) int {
     return x + y;
}

print add(2, 3+4);
    """
    )

    assert str(statements[0]) == (
        "Function(name=Name(text='add'),"
        + " parameter_names=[Name(text='x'),"
        + " Name(text='y')],"
        + " parameter_types=[Type(type_enum=<TypeEnum.INT: 'INT'>),"
        + " Type(type_enum=<TypeEnum.INT: 'INT'>)],"
        + " return_type=Type(type_enum=<TypeEnum.INT: 'INT'>),"
        + " body=Block(statements=[Return(expression=Binary(left=Name(text='x'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Name(text='y')))]))"
    )
    assert str(statements[1]) == (
        "Print(expression=Call(callee=Name(text='add'),"
        + " arguments=[Integer(value='2'),"
        + " Binary(left=Integer(value='3'),"
        + " operator_enum=<OperatorEnum.PLUS: '+'>,"
        + " right=Integer(value='4'))]))"
    )
