from format import format
from model import *


def test_format():
    # program 1
    assert format(Print(Integer("42"))) == "print 42;\n"

    # program 2
    assert format(Print(Binary(Integer("2"), "+", Integer("3")))) == "print 2 + 3;\n"
    assert (
        format(Print(Binary(Unary("-", Integer("2")), "+", Integer("3"))))
        == "print -2 + 3;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Integer("2"),
                    "+",
                    Binary(Integer("3"), "*", Unary("-", Integer("4"))),
                )
            )
        )
        == "print 2 + 3 * -4;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Grouping(Binary(Integer("2"), "+", Integer("3"))), "*", Integer("4")
                )
            )
        )
        == "print (2 + 3) * 4;\n"
    )
    assert (
        format(
            Print(Binary(Float("2.0"), "-", Binary(Float("3.0"), "/", Float("4.0"))))
        )
        == "print 2.0 - 3.0 / 4.0;\n"
    )
