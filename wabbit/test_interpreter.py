from interpreter import Value, evaluate
from expression import TypeEnum, OperatorEnum, Integer, Binary, Float, Grouping, Unary


def test_evaluate_primitives():
    # program 1
    assert evaluate(Integer("42")) == Value(TypeEnum.INT, 42)

    # program 2
    assert evaluate(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))) == Value(
        TypeEnum.INT, 5
    )
    assert evaluate(
        Binary(
            Unary(OperatorEnum.MINUS, Integer("2")),
            OperatorEnum.PLUS,
            Integer("3"),
        )
    ) == Value(TypeEnum.INT, 1)
    assert evaluate(
        Binary(
            Integer("2"),
            OperatorEnum.PLUS,
            Binary(
                Integer("3"),
                OperatorEnum.TIMES,
                Unary(OperatorEnum.MINUS, Integer("4")),
            ),
        )
    ) == Value(TypeEnum.INT, -10)
    assert evaluate(
        Binary(
            Grouping(Binary(Integer("2"), OperatorEnum.PLUS, Integer("3"))),
            OperatorEnum.TIMES,
            Integer("4"),
        )
    ) == Value(TypeEnum.INT, 20)
    assert evaluate(
        Binary(
            Float("2.0"),
            OperatorEnum.MINUS,
            Binary(Float("3.0"), OperatorEnum.DIVIDE, Float("4.0")),
        )
    ) == Value(TypeEnum.FLOAT, 1.25)
