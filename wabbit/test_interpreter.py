from interpreter import WValue, evaluate
from expression import TypeEnum, Integer


def test_evaluate_primitives():
    assert evaluate(Integer("42")) == WValue(TypeEnum.INT, 42)
