from format import format
from model import *


if __name__ == "__main__":
    # program 1
    print(format(Print(Literal(42))))

    # program 2
    print(format(Print(Binary(Literal(2), "+", Literal(3)))), end="")
    print(format(Print(Binary(Unary("-", Literal(2)), "+", Literal(3)))), end="")
    print(
        format(
            Print(
                Binary(
                    Literal(2), "+", Binary(Literal(3), "*", Unary("-", Literal("4")))
                )
            )
        ),
        end="",
    )
    print(
        format(
            Print(
                Binary(Grouping(Binary(Literal(2), "+", Literal(3))), "*", Literal(4))
            )
        ),
        end="",
    )
    print(
        format(
            Print(Binary(Literal(2.0), "-", Binary(Literal(3.0), "/", Literal("4.0"))))
        ),
    )

    # program 3
    print(format(Assign(Constant(Name("pi")), Literal(3.14159))), end="")
    print(
        format(Assign(Constant(Name("tau")), Binary(Literal(2.0), "*", Name("pi")))),
        end="",
    )
    print(format(Assign(Variable(Name("radius")), Literal(4.0))), end="")
    print(format(Type(Variable(Name("perimeter")), "float")), end="")
    print(
        format(Assign(Name("perimeter"), Binary(Name("tau"), "*", Name("radius")))),
        end="",
    )
    print(format(Print(Name("perimeter"))))
