from format import format
from model import *


if __name__ == "__main__":
    # program 1
    print(format(Print(Integer("42"))))

    # # program 2
    print(format(Print(Binary(Integer("2"), "+", Integer("3")))), end="")
    print(format(Print(Binary(Unary("-", Integer("2")), "+", Integer("3")))), end="")
    print(
        format(
            Print(
                Binary(
                    Integer("2"),
                    "+",
                    Binary(Integer("3"), "*", Unary("-", Integer("4"))),
                )
            )
        ),
        end="",
    )
    print(
        format(
            Print(
                Binary(
                    Grouping(Binary(Integer("2"), "+", Integer("3"))), "*", Integer("4")
                )
            )
        ),
        end="",
    )
    print(
        format(
            Print(Binary(Float("2.0"), "-", Binary(Float("3.0"), "/", Float("4.0"))))
        ),
    )

    # program 3
    print(format(ConstantDeclaration(Name("pi"), None, Float("3.14159"))), end="")
    print(
        format(
            ConstantDeclaration(
                Name("tau"), None, Binary(Float("2.0"), "*", Name("pi"))
            )
        ),
        end="",
    )
    print(format(VariableDeclaration(Name("radius"), None, Float("4.0"))), end="")
    print(
        format(VariableDeclaration(Name("perimeter"), TypeName("float"), None)), end=""
    )
    print(
        format(Assign(Name("perimeter"), Binary(Name("tau"), "*", Name("radius")))),
        end="",
    )
    print(format(Print(Name("perimeter"))), end="")
