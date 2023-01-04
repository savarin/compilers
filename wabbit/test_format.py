from format import format
from model import Binary, Grouping, Literal, Print, Unary


def test_format():
    # program 1
    assert format(Print(Literal(42))) == "print 42;\n"

    # program 2
    assert format(Print(Binary(Literal(2), "+", Literal(3)))) == "print 2 + 3;\n"
    assert (
        format(Print(Binary(Unary("-", Literal(2)), "+", Literal(3))))
        == "print -2 + 3;\n"
    )
    assert (
        format(
            Print(
                Binary(
                    Literal(2), "+", Binary(Literal(3), "*", Unary("-", Literal("4")))
                )
            )
        )
        == "print 2 + 3 * -4;\n"
    )
    assert (
        format(
            Print(
                Binary(Grouping(Binary(Literal(2), "+", Literal(3))), "*", Literal(4))
            )
        )
        == "print (2 + 3) * 4;\n"
    )
    assert (
        format(
            Print(Binary(Literal(2.0), "-", Binary(Literal(3.0), "/", Literal("4.0"))))
        )
        == "print 2.0 - 3.0 / 4.0;\n"
    )
