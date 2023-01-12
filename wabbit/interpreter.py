from typing import Union
import dataclasses

from expression import (
    Expr,
    TypeEnum,
    OperatorEnum,
    Boolean,
    Float,
    Grouping,
    Integer,
    Binary,
    Unary,
)


@dataclasses.dataclass
class Value:
    type: TypeEnum
    py_value: Union[bool, float, int]


def evaluate(expression: Expr) -> Value:  # type: ignore[return]
    match expression:
        case Boolean(value):
            return Value(TypeEnum.BOOL, bool(value))

        case Float(value):
            return Value(TypeEnum.FLOAT, float(value))

        case Integer(value):
            return Value(TypeEnum.INT, int(value))

        case Binary(left, operator_enum, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)

            assert left_eval.type == right_eval.type

            if operator_enum == OperatorEnum.PLUS:
                if left_eval.type == TypeEnum.FLOAT:
                    return Value(
                        TypeEnum.FLOAT, left_eval.py_value + right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return Value(TypeEnum.INT, left_eval.py_value + right_eval.py_value)

            elif operator_enum == OperatorEnum.MINUS:
                if left_eval.type == TypeEnum.FLOAT:
                    return Value(
                        TypeEnum.FLOAT, left_eval.py_value - right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return Value(TypeEnum.INT, left_eval.py_value - right_eval.py_value)

            elif operator_enum == OperatorEnum.TIMES:
                if left_eval.type == TypeEnum.FLOAT:
                    return Value(
                        TypeEnum.FLOAT, left_eval.py_value * right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return Value(TypeEnum.INT, left_eval.py_value * right_eval.py_value)

            elif operator_enum == OperatorEnum.DIVIDE:
                if left_eval.type == TypeEnum.FLOAT:
                    return Value(
                        TypeEnum.FLOAT, left_eval.py_value / right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return Value(
                        TypeEnum.INT, left_eval.py_value // right_eval.py_value
                    )

        case Grouping(expression):
            return evaluate(expression)

        case Unary(operator_enum, right):
            right_eval = evaluate(right)

            if operator_enum == OperatorEnum.MINUS:
                if right_eval.type == TypeEnum.FLOAT:
                    return Value(TypeEnum.FLOAT, -right_eval.py_value)

                elif right_eval.type == TypeEnum.INT:
                    return Value(TypeEnum.INT, -right_eval.py_value)

        case _:
            raise Exception("Exhaustive switch error.")
