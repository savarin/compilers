from format import format
from expression import *
from statement import *


if __name__ == "__main__":
    # program 1
    print(format(Print(Integer("42"))))

    # # program 2
    print(format(Print(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3")))), end="")
    print(
        format(
            Print(
                Binary(
                    Unary(OperatorEnum.MINUS, Integer("2")),
                    OperatorEnum.PLUS,
                    Integer("3"),
                )
            )
        ),
        end="",
    )
    print(
        format(
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
        ),
        end="",
    )
    print(
        format(
            Print(
                Binary(
                    Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
                    OperatorEnum.TIMES,
                    Integer("4"),
                )
            )
        ),
        end="",
    )
    print(
        format(
            Print(
                Binary(
                    Float("2.0"),
                    OperatorEnum.MINUS,
                    Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
                )
            )
        ),
    )

    # program 3
    print(
        format(Declaration(Name("pi"), DeclarationEnum.CONST, None, Float("3.14159"))),
        end="",
    )
    print(
        format(
            Declaration(
                Name("tau"),
                DeclarationEnum.CONST,
                None,
                Binary(Float("2.0"), OperatorEnum.MINUS, Name("pi")),
            )
        ),
        end="",
    )
    print(
        format(Declaration(Name("radius"), DeclarationEnum.VAR, None, Float("4.0"))),
        end="",
    )
    print(
        format(
            Declaration(
                Name("perimeter"), DeclarationEnum.VAR, Type(TypeEnum.FLOAT), None
            )
        ),
        end="",
    )
    print(
        format(
            Expression(
                Assign(
                    Name("perimeter"),
                    Binary(Name("tau"), OperatorEnum.TIMES, Name("radius")),
                )
            )
        ),
        end="",
    )
    print(format(Print(Name("perimeter"))))

    # program 4
    print(format(Print(Boolean("true"))), end="")
    print(format(Print(Binary(Integer("1"), OperatorEnum.EQ_EQ, Integer("1")))), end="")
    print(format(Print(Binary(Integer("0"), OperatorEnum.LESS, Integer("1")))), end="")
    print(format(Print(Binary(Integer("1"), OperatorEnum.GREAT, Integer("0")))), end="")
    print(
        format(Print(Binary(Boolean("true"), OperatorEnum.AND, Boolean("true")))),
        end="",
    )
    print(
        format(Print(Binary(Boolean("false"), OperatorEnum.OR, Boolean("true")))),
        end="",
    )
    print(format(Print(Unary(OperatorEnum.NOT, Boolean("false")))))
