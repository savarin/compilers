from interpreter import Value, evaluate, init_environment, init_interpreter, interpret
from expression import (
    TypeEnum,
    OperatorEnum,
    Boolean,
    Integer,
    Float,
    Name,
    Type,
    Assign,
    Binary,
    Call,
    Grouping,
    Unary,
)
from statement import (
    DeclarationEnum,
    Block,
    Break,
    Continue,
    Declaration,
    Expression,
    Function,
    If,
    Print,
    Return,
    While,
)


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

    assert interpret(init_interpreter(statements)) == ["-4.5663599999999995"]

    # program 4
    assert evaluate(environment, Boolean("true"))[1] == Value(TypeEnum.BOOL, True)
    assert evaluate(
        environment, Binary(Integer("1"), OperatorEnum.EQUAL_EQUAL, Integer("1"))
    )[1] == Value(TypeEnum.BOOL, True)
    assert evaluate(environment, Binary(Integer("0"), OperatorEnum.LESS, Integer("1")))[
        1
    ] == Value(TypeEnum.BOOL, True)
    assert evaluate(
        environment, Binary(Integer("1"), OperatorEnum.GREATER, Integer("0"))
    )[1] == Value(TypeEnum.BOOL, True)
    assert evaluate(
        environment, Binary(Boolean("true"), OperatorEnum.AND, Boolean("true"))
    )[1] == Value(TypeEnum.BOOL, True)
    assert evaluate(
        environment, Binary(Boolean("false"), OperatorEnum.OR, Boolean("true"))
    )[1] == Value(TypeEnum.BOOL, True)
    assert evaluate(environment, Unary(OperatorEnum.NOT, Boolean("false")))[1] == Value(
        TypeEnum.BOOL, True
    )

    # program 5
    statements = [
        Declaration(Name("a"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("2")),
        Declaration(Name("b"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("3")),
        Declaration(Name("minval"), DeclarationEnum.VAR, Type(TypeEnum.INT), None),
        If(
            Binary(Name("a"), OperatorEnum.LESS, Name("b")),
            Block([Expression(Assign(Name("minval"), Name("a")))]),
            Block([Expression(Assign(Name("minval"), Name("b")))]),
        ),
        Print(Name("minval")),
    ]

    assert interpret(init_interpreter(statements)) == ["2"]

    # program 6
    statements = [
        Declaration(Name("x"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")),
        Declaration(
            Name("fact"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")
        ),
        While(
            Binary(Name("x"), OperatorEnum.LESS, Integer("7")),
            Block(
                [
                    Expression(
                        Assign(
                            Name("fact"),
                            Binary(Name("fact"), OperatorEnum.TIMES, Name("x")),
                        )
                    ),
                    Expression(
                        Assign(
                            Name("x"),
                            Binary(Name("x"), OperatorEnum.PLUS, Integer("1")),
                        )
                    ),
                    Print(Name("fact")),
                ]
            ),
        ),
    ]

    assert interpret(init_interpreter(statements)) == [
        "1",
        "2",
        "6",
        "24",
        "120",
        "720",
    ]

    # program 7
    statements = [
        Declaration(Name("n"), DeclarationEnum.VAR, None, Integer("5")),
        While(
            Boolean("true"),
            Block(
                [
                    If(
                        Binary(Name("n"), OperatorEnum.EQUAL_EQUAL, Integer("0")),
                        Block([Break()]),
                        Block(
                            [
                                Print(Name("n")),
                                Expression(
                                    Assign(
                                        Name("n"),
                                        Binary(
                                            Name("n"),
                                            OperatorEnum.MINUS,
                                            Integer("1"),
                                        ),
                                    )
                                ),
                                Continue(),
                            ]
                        ),
                    ),
                    Expression(
                        Assign(
                            Name("n"),
                            Binary(Name("n"), OperatorEnum.PLUS, Integer("1")),
                        )
                    ),
                ],
            ),
        ),
    ]

    assert interpret(init_interpreter(statements)) == ["5", "4", "3", "2", "1"]

    # program 8
    statements = [
        Function(
            Name("add"),
            [Name("x"), Name("y")],
            [Type(TypeEnum.INT), Type(TypeEnum.INT)],
            Type(TypeEnum.INT),
            Block([Return(Binary(Name("x"), OperatorEnum.PLUS, Name("y")))]),
        ),
        Declaration(
            Name("result"),
            DeclarationEnum.VAR,
            None,
            Call(Name("add"), [Integer("2"), Integer("3")]),
        ),
        Print(Name("result")),
    ]

    assert interpret(init_interpreter(statements)) == ["5"]
