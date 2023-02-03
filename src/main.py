from format import format
from expression import (
    TypeEnum,
    OperatorEnum,
    Boolean,
    Float,
    Integer,
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
    Statem,
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


def f(statement: Statem, newline: bool = False):
    return print(format(statement), end="\n" if newline else "")


if __name__ == "__main__":
    # program 1
    f(Print(Integer("42")), True)

    # program 2
    f(Print(Binary(Integer("2"), OperatorEnum.TIMES, Integer("3"))))
    f(
        Print(
            Binary(
                Unary(OperatorEnum.MINUS, Integer("2")),
                OperatorEnum.PLUS,
                Integer("3"),
            )
        )
    )
    f(
        Print(
            Binary(
                Integer("2"),
                OperatorEnum.PLUS,
                Binary(
                    Integer("3"),
                    OperatorEnum.TIMES,
                    Unary(OperatorEnum.MINUS, Integer("4")),
                ),
            )
        )
    )
    f(
        Print(
            Binary(
                Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
                OperatorEnum.TIMES,
                Integer("4"),
            )
        )
    )
    f(
        Print(
            Binary(
                Float("2.0"),
                OperatorEnum.MINUS,
                Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
            )
        ),
        True,
    )

    # program 3
    f(Declaration(Name("pi"), DeclarationEnum.CONST, None, Float("3.14159")))
    f(
        Declaration(
            Name("tau"),
            DeclarationEnum.CONST,
            None,
            Binary(Float("2.0"), OperatorEnum.MINUS, Name("pi")),
        )
    )
    f(Declaration(Name("radius"), DeclarationEnum.VAR, None, Float("4.0")))
    f(Declaration(Name("perimeter"), DeclarationEnum.VAR, Type(TypeEnum.FLOAT), None))
    f(
        Expression(
            Assign(
                Name("perimeter"),
                Binary(Name("tau"), OperatorEnum.TIMES, Name("radius")),
            )
        )
    )
    f(Print(Name("perimeter")), True)

    # program 4
    f(Print(Boolean("true")))
    f(Print(Binary(Integer("1"), OperatorEnum.EQUAL_EQUAL, Integer("1"))))
    f(Print(Binary(Integer("0"), OperatorEnum.LESS, Integer("1"))))
    f(Print(Binary(Integer("1"), OperatorEnum.GREATER, Integer("0"))))
    f(Print(Binary(Boolean("true"), OperatorEnum.AND, Boolean("true"))))
    f(Print(Binary(Boolean("false"), OperatorEnum.OR, Boolean("true"))))
    f(Print(Unary(OperatorEnum.NOT, Boolean("false"))), True)

    # program 5
    f(Declaration(Name("a"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("2")))
    f(Declaration(Name("b"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("3")))
    f(Declaration(Name("minval"), DeclarationEnum.VAR, Type(TypeEnum.INT), None))
    f(
        If(
            Binary(Name("a"), OperatorEnum.LESS, Name("b")),
            Block([Expression(Assign(Name("minval"), Name("a")))]),
            Block([Expression(Assign(Name("minval"), Name("b")))]),
        )
    )
    f(Print(Name("minval")), True)

    # program 6
    f(Declaration(Name("x"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")))
    f(Declaration(Name("fact"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")))
    f(
        While(
            Binary(Name("x"), OperatorEnum.LESS, Integer("11")),
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
        True,
    )

    # program 7
    f(Declaration(Name("n"), DeclarationEnum.VAR, None, Integer("5")))
    f(
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
                                            Name("n"), OperatorEnum.MINUS, Integer("1")
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
        True,
    )

    # program 8
    f(
        Function(
            Name("add"),
            [Name("x"), Name("y")],
            [Type(TypeEnum.INT), Type(TypeEnum.INT)],
            Type(TypeEnum.INT),
            Block([Return(Binary(Name("x"), OperatorEnum.PLUS, Name("y")))]),
        )
    )
    f(
        Declaration(
            Name("result"),
            DeclarationEnum.VAR,
            None,
            Call(Name("add"), [Integer("2"), Integer("3")]),
        )
    )
    f(Print(Name("result")), True)
