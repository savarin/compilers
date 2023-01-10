from format import format
from expression import (
    Expr,
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

    # program 3
    assert (
        format(Declaration(Name("pi"), DeclarationEnum.CONST, None, Float("3.14159")))
        == "const pi = 3.14159;\n"
    )
    assert (
        format(
            Declaration(
                Name("tau"),
                DeclarationEnum.CONST,
                None,
                Binary(Float("2.0"), OperatorEnum.MINUS, Name("pi")),
            )
        )
        == "const tau = 2.0 - pi;\n"
    )
    assert (
        format(Declaration(Name("radius"), DeclarationEnum.VAR, None, Float("4.0")))
        == "var radius = 4.0;\n"
    )
    assert (
        format(
            Declaration(
                Name("perimeter"), DeclarationEnum.VAR, Type(TypeEnum.FLOAT), None
            )
        )
        == "var perimeter float;\n"
    )
    assert (
        format(
            Expression(
                Assign(
                    Name("perimeter"),
                    Binary(Name("tau"), OperatorEnum.TIMES, Name("radius")),
                )
            )
        )
        == "perimeter = tau * radius;\n"
    )
    assert format(Print(Name("perimeter"))) == "print perimeter;\n"

    # program 4
    assert format(Print(Boolean("true"))) == "print true;\n"
    assert (
        format(Print(Binary(Integer("1"), OperatorEnum.EQUAL_EQUAL, Integer("1"))))
        == "print 1 == 1;\n"
    )
    assert (
        format(Print(Binary(Integer("0"), OperatorEnum.LESS, Integer("1"))))
        == "print 0 < 1;\n"
    )
    assert (
        format(Print(Binary(Integer("1"), OperatorEnum.GREATER, Integer("0"))))
        == "print 1 > 0;\n"
    )
    assert (
        format(Print(Binary(Boolean("true"), OperatorEnum.AND, Boolean("true"))))
        == "print true && true;\n"
    )
    assert (
        format(Print(Binary(Boolean("false"), OperatorEnum.OR, Boolean("true"))))
        == "print false || true;\n"
    )
    assert format(Print(Unary(OperatorEnum.NOT, Boolean("false")))) == "print !false;\n"

    # program 5
    assert (
        format(
            Declaration(
                Name("a"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("2")
            )
        )
        == "var a int = 2;\n"
    )
    assert (
        format(
            Declaration(
                Name("b"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("3")
            )
        )
        == "var b int = 3;\n"
    )
    assert (
        format(
            Declaration(Name("minval"), DeclarationEnum.VAR, Type(TypeEnum.INT), None)
        )
        == "var minval int;\n"
    )
    abra = (
        format(
            If(
                Binary(Name("a"), OperatorEnum.LESS, Name("b")),
                Block([Expression(Assign(Name("minval"), Name("a")))]),
                Block([Expression(Assign(Name("minval"), Name("b")))]),
            )
        )
        == """\
if a < b {
    minval = a;
} else {
    minval = b;
}\n"""
    )
    assert format(Print(Name("minval"))) == "print minval;\n"

    # program 6
    assert (
        format(
            Declaration(
                Name("x"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")
            )
        )
        == "var x int = 1;\n"
    )
    assert (
        format(
            Declaration(
                Name("fact"), DeclarationEnum.VAR, Type(TypeEnum.INT), Integer("1")
            )
        )
        == "var fact int = 1;\n"
    )
    assert (
        format(
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
        )
        == """\
while x < 11 {
    fact = fact * x;
    x = x + 1;
    print fact;
}\n"""
    )

    # program 7
    assert (
        format(Declaration(Name("n"), DeclarationEnum.VAR, None, Integer("5")))
        == "var n = 5;\n"
    )
    assert (
        format(
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
        )
        == """\
while true {
    if n == 0 {
        break;
    } else {
        print n;
        n = n - 1;
        continue;
    }
    n = n + 1;
}\n"""
    )

    # program 8
    assert (
        format(
            Function(
                Name("add"),
                [Name("x"), Name("y")],
                [Type(TypeEnum.INT), Type(TypeEnum.INT)],
                Type(TypeEnum.INT),
                Block([Return(Binary(Name("x"), OperatorEnum.PLUS, Name("y")))]),
            )
        )
        == """\
func add(x int, y int) int {
    return x + y;
}\n"""
    )
    assert (
        format(
            Declaration(
                Name("result"),
                DeclarationEnum.VAR,
                None,
                Call(Name("add"), [Integer("2"), Integer("3")]),
            )
        )
        == "var result = add(2, 3);\n"
    )
    assert format(Print(Name("result"))) == "print result;\n"
