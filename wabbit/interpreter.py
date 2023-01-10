from typing import Union
import dataclasses

from expression import Expr, TypeEnum, Boolean, Float, Integer


@dataclasses.dataclass
class WValue:
    w_type: TypeEnum
    p_value: Union[bool, float, int]


def evaluate(expression: Expr) -> WValue:
    match expression:
        case Boolean(value):
            return WValue(TypeEnum.BOOL, bool(value))

        case Float(value):
            return WValue(TypeEnum.FLOAT, float(value))

        case Integer(value):
            return WValue(TypeEnum.INT, int(value))

        case _:
            raise Exception("Exhaustive switch error.")
