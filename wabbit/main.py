from format import format
from model import Binary, Grouping, Literal, Print, Unary


if __name__ == "__main__":
    # program 1
    print(format(Print(Literal(42))))

    # program 2
    print(format(Print(Binary(Literal(2), "+", Literal(3)))))
    print(format(Print(Binary(Unary("-", Literal(2)), "+", Literal(3)))))
    print(
        format(
            Print(
                Binary(
                    Literal(2), "+", Binary(Literal(3), "*", Unary("-", Literal("4")))
                )
            )
        )
    )
    print(
        format(
            Print(
                Binary(Grouping(Binary(Literal(2), "+", Literal(3))), "*", Literal(4))
            )
        )
    )
    print(
        format(
            Print(Binary(Literal(2.0), "-", Binary(Literal(3.0), "/", Literal("4.0"))))
        )
    )
