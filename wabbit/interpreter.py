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
class WValue:
    w_type: TypeEnum
    p_value: Union[bool, float, int]


def evaluate(expression: Expr) -> WValue:  # type: ignore[return]
    match expression:
        case Boolean(value):
            return WValue(TypeEnum.BOOL, bool(value))

        case Float(value):
            return WValue(TypeEnum.FLOAT, float(value))

        case Integer(value):
            return WValue(TypeEnum.INT, int(value))

        case Binary(left, operator_enum, right):
            left_eval = evaluate(left)
            right_eval = evaluate(right)

            assert left_eval.w_type == right_eval.w_type

            if operator_enum == OperatorEnum.PLUS:
                if left_eval.w_type == TypeEnum.FLOAT:
                    return WValue(
                        TypeEnum.FLOAT, left_eval.p_value + right_eval.p_value
                    )

                elif left_eval.w_type == TypeEnum.INT:
                    return WValue(TypeEnum.INT, left_eval.p_value + right_eval.p_value)

            elif operator_enum == OperatorEnum.MINUS:
                if left_eval.w_type == TypeEnum.FLOAT:
                    return WValue(
                        TypeEnum.FLOAT, left_eval.p_value - right_eval.p_value
                    )

                elif left_eval.w_type == TypeEnum.INT:
                    return WValue(TypeEnum.INT, left_eval.p_value - right_eval.p_value)

            elif operator_enum == OperatorEnum.TIMES:
                if left_eval.w_type == TypeEnum.FLOAT:
                    return WValue(
                        TypeEnum.FLOAT, left_eval.p_value * right_eval.p_value
                    )

                elif left_eval.w_type == TypeEnum.INT:
                    return WValue(TypeEnum.INT, left_eval.p_value * right_eval.p_value)

            elif operator_enum == OperatorEnum.DIVIDE:
                if left_eval.w_type == TypeEnum.FLOAT:
                    return WValue(
                        TypeEnum.FLOAT, left_eval.p_value / right_eval.p_value
                    )

                elif left_eval.w_type == TypeEnum.INT:
                    return WValue(TypeEnum.INT, left_eval.p_value // right_eval.p_value)

        case Grouping(expression):
            return evaluate(expression)

        case Unary(operator_enum, right):
            right_eval = evaluate(right)

            if operator_enum == OperatorEnum.MINUS:
                if right_eval.w_type == TypeEnum.FLOAT:
                    return WValue(TypeEnum.FLOAT, -right_eval.p_value)

                elif right_eval.w_type == TypeEnum.INT:
                    return WValue(TypeEnum.INT, -right_eval.p_value)

        case _:
            raise Exception("Exhaustive switch error.")
