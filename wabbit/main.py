from format import format
from expression import *
from statement import *


def p(statement, end=""):
    return print(format(statement), end=end)


if __name__ == "__main__":
    # program 1
    p(Print(Integer("42")), "\n")

    # # program 2
    p(Print(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))))
    p(
        Print(
            Binary(
                Unary(OperatorEnum.MINUS, Integer("2")),
                OperatorEnum.PLUS,
                Integer("3"),
            )
        )
    )
    p(
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
    p(
        Print(
            Binary(
                Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
                OperatorEnum.TIMES,
                Integer("4"),
            )
        )
    )
    p(
        Print(
            Binary(
                Float("2.0"),
                OperatorEnum.MINUS,
                Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
            )
        ),
        "\n",
    )

    # program 3
    p(Declaration(Name("pi"), DeclarationEnum.CONST, None, Float("3.14159")))
    p(
        Declaration(
            Name("tau"),
            DeclarationEnum.CONST,
            None,
            Binary(Float("2.0"), OperatorEnum.MINUS, Name("pi")),
        )
    )
    p(Declaration(Name("radius"), DeclarationEnum.VAR, None, Float("4.0")))
    p(Declaration(Name("perimeter"), DeclarationEnum.VAR, Type(TypeEnum.FLOAT), None))
    p(
        Expression(
            Assign(
                Name("perimeter"),
                Binary(Name("tau"), OperatorEnum.TIMES, Name("radius")),
            )
        )
    )
    p(Print(Name("perimeter")), "\n")

    # program 4
    p(Print(Boolean("true")))
    p(Print(Binary(Integer("1"), OperatorEnum.EQ_EQ, Integer("1"))))
    p(Print(Binary(Integer("0"), OperatorEnum.LESS, Integer("1"))))
    p(Print(Binary(Integer("1"), OperatorEnum.GREAT, Integer("0"))))
    print(
        format(Print(Binary(Boolean("true"), OperatorEnum.AND, Boolean("true")))),
        end="",
    )
    print(
        format(Print(Binary(Boolean("false"), OperatorEnum.OR, Boolean("true")))),
        end="",
    )
    p(Print(Unary(OperatorEnum.NOT, Boolean("false"))), "\n")

    # program 5
    p(Declaration(Name("a"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("2")))
    p(Declaration(Name("b"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("3")))
    p(Declaration(Name("minval"), DeclarationEnum.VAR, Type(TypeEnum.INT), None))
    p(
        If(
            Binary(Name("a"), OperatorEnum.LESS, Name("b")),
            Block([Expression(Assign(Name("minval"), Name("a")))]),
            Block([Expression(Assign(Name("minval"), Name("b")))]),
        )
    )
    p(Print(Name("minval")), "\n")

    # program 6
    p(Declaration(Name("x"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")))
    p(Declaration(Name("fact"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")))
    p(
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
        "\n",
    )

    # program 7
    p(Declaration(Name("n"), DeclarationEnum.VAR, None, Integer("5")))
    p(
        While(
            Boolean("true"),
            Block(
                [
                    If(
                        Binary(Name("n"), OperatorEnum.EQ_EQ, Integer("0")),
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
        "\n",
    )

    # program 8
    p(
        Function(
            Name("add"),
            [Name("x"), Name("y")],
            [Type(TypeEnum.INT), Type(TypeEnum.INT)],
            Type(TypeEnum.INT),
            Block([Return(Binary(Name("x"), OperatorEnum.PLUS, Name("y")))]),
        )
    )
    p(
        Declaration(
            Name("result"),
            DeclarationEnum.VAR,
            None,
            Call(Name("add"), [Integer("2"), Integer("3")]),
        )
    )
    p(Print(Name("result")), "\n")
