from interpreter import Value, evaluate, init_environment, init_interpreter, interpret
from expression import (
    TypeEnum,
    OperatorEnum,
    Integer,
    Float,
    Name,
    Type,
    Assign,
    Binary,
    Grouping,
    Unary,
)
from statement import DeclarationEnum, Declaration, Expression, Print


def test_evaluate():
    environment = init_environment()

    # program 1
    assert evaluate(environment, Integer("42"))[1] == Value(TypeEnum.INT, 42)

    # program 2
    assert evaluate(environment, Binary(Integer("2"), OperatorEnum.PLUS, Integer("3")))[
        1
    ] == Value(TypeEnum.INT, 5)
    assert evaluate(
        environment,
        Binary(
            Unary(OperatorEnum.MINUS, Integer("2")),
            OperatorEnum.PLUS,
            Integer("3"),
        ),
    )[1] == Value(TypeEnum.INT, 1)
    assert evaluate(
        environment,
        Binary(
            Integer("2"),
            OperatorEnum.PLUS,
            Binary(
                Integer("3"),
                OperatorEnum.TIMES,
                Unary(OperatorEnum.MINUS, Integer("4")),
            ),
        ),
    )[1] == Value(TypeEnum.INT, -10)
    assert evaluate(
        environment,
        Binary(
            Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
            OperatorEnum.TIMES,
            Integer("4"),
        ),
    )[1] == Value(TypeEnum.INT, 20)
    assert evaluate(
        environment,
        Binary(
            Float("2.0"),
            OperatorEnum.MINUS,
            Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
        ),
    )[1] == Value(TypeEnum.FLOAT, 1.25)

    # program 3
    statements = [
        Declaration(Name("pi"), DeclarationEnum.CONST, None, Float("3.14159")),
        Declaration(
            Name("tau"),
            DeclarationEnum.CONST,
            None,
            Binary(Float("2.0"), OperatorEnum.MINUS, Name("pi")),
        ),
        Declaration(Name("radius"), DeclarationEnum.VAR, None, Float("4.0")),
        Declaration(Name("perimeter"), DeclarationEnum.VAR, Type(TypeEnum.FLOAT), None),
        Expression(
            Assign(
                Name("perimeter"),
                Binary(Name("tau"), OperatorEnum.TIMES, Name("radius")),
            )
        ),
        Print(Name("perimeter")),
    ]

    interpreter = init_interpreter(statements)
    assert interpret(interpreter) == ["-4.5663599999999995"]
