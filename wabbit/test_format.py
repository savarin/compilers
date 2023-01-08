from format import format
from expression import *
from statement import *


def test_format():
    # program 1
    assert format(Print(Integer("42"))) == "print 42;\n"

    # program 2
    assert (
        format(Print(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))))
        == "print 2 + 3;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Unary(OperatorEnum.MINUS, Integer("2")),
                    OperatorEnum.PLUS,
                    Integer("3"),
                )
            )
        )
        == "print -2 + 3;\n"
    )
    assert (
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
        )
        == "print 2 + 3 * -4;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
                    OperatorEnum.TIMES,
                    Integer("4"),
                )
            )
        )
        == "print (2 + 3) * 4;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Float("2.0"),
                    OperatorEnum.MINUS,
                    Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
                )
            )
        )
        == "print 2.0 - 3.0 / 4.0;\n"
    )
