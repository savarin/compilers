from typing import Dict, List, Optional, Tuple, Union
import dataclasses

from expression import (
    TypeEnum,
    OperatorEnum,
    Expr,
    Boolean,
    Float,
    Name,
    Assign,
    Grouping,
    Integer,
    Binary,
    Unary,
)
from statement import Declaration, Expression, Print, Statem


@dataclasses.dataclass
class Value:
    type: TypeEnum
    py_value: Union[bool, float, int]


@dataclasses.dataclass
class Environment:
    values: Dict[str, Optional[Value]]


def init_environment() -> Environment:
    values: Dict[str, Optional[Value]] = {}
    return Environment(values)


def define(environment: Environment, name: str, value: Optional[Value]) -> Environment:
    environment.values[name] = value
    return environment


def get(environment: Environment, name: str) -> Optional[Value]:
    if name in environment.values:
        return environment.values[name]

    raise Exception("Name not found.")


def assign(environment: Environment, name: str, value: Optional[Value]) -> Environment:
    if name in environment.values:
        environment.values[name] = value
        return environment

    raise Exception("Name not found.")


@dataclasses.dataclass
class Interpreter:
    statements: List[Statem]
    environment: Environment


def init_interpreter(statements: List[Statem]) -> Interpreter:
    environment = init_environment()
    return Interpreter(statements, environment)


def interpret(interpreter: Interpreter) -> List[str]:
    result: List[str] = []

    for statement in interpreter.statements:
        interpreter, individual_result = execute(interpreter, statement)
        result += individual_result

    return result


def execute(  # type: ignore[return]
    interpreter: Interpreter, statement: Statem
) -> Tuple[Interpreter, List[str]]:
    match statement:
        # TODO: Implement storing of const vs var type.
        case Declaration(name, _, _, initializer):
            value = None

            if initializer is not None:
                environment, value = evaluate(interpreter.environment, initializer)

            interpreter.environment = define(interpreter.environment, name.text, value)
            return interpreter, []

        case Expression(expression):
            interpreter.environment, result = evaluate(
                interpreter.environment, expression
            )

            if isinstance(result, list):
                return interpreter, result

            return interpreter, []

        case Print(expression):
            interpreter.environment, result = evaluate(
                interpreter.environment, expression
            )

            if isinstance(result, list):
                return interpreter, result

            assert result is not None
            return interpreter, [str(result.py_value or "nil")]

        case _:
            raise Exception("Exhaustive switch error.")


def evaluate(  # type: ignore[return]
    environment: Environment, expression: Expr
) -> Tuple[Environment, Optional[Value]]:
    match expression:
        case Boolean(value):
            return environment, Value(
                TypeEnum.BOOL, {"true": True, "false": False}[value]
            )

        case Float(value):
            return environment, Value(TypeEnum.FLOAT, float(value))

        case Integer(value):
            return environment, Value(TypeEnum.INT, int(value))

        case Name(text):
            return environment, get(environment, text)

        case Assign(name, value):
            environment, result = evaluate(environment, value)
            return assign(environment, name.text, result), None

        case Binary(left, operator_enum, right):
            environment, left_eval = evaluate(environment, left)
            environment, right_eval = evaluate(environment, right)
            assert left_eval is not None and right_eval is not None

            assert left_eval.type == right_eval.type

            if operator_enum == OperatorEnum.PLUS:
                if left_eval.type == TypeEnum.FLOAT:
                    return environment, Value(
                        TypeEnum.FLOAT, left_eval.py_value + right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return environment, Value(
                        TypeEnum.INT, left_eval.py_value + right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.MINUS:
                if left_eval.type == TypeEnum.FLOAT:
                    return environment, Value(
                        TypeEnum.FLOAT, left_eval.py_value - right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return environment, Value(
                        TypeEnum.INT, left_eval.py_value - right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.TIMES:
                if left_eval.type == TypeEnum.FLOAT:
                    return environment, Value(
                        TypeEnum.FLOAT, left_eval.py_value * right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return environment, Value(
                        TypeEnum.INT, left_eval.py_value * right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.DIVIDE:
                if left_eval.type == TypeEnum.FLOAT:
                    return environment, Value(
                        TypeEnum.FLOAT, left_eval.py_value / right_eval.py_value
                    )

                elif left_eval.type == TypeEnum.INT:
                    return environment, Value(
                        TypeEnum.INT, left_eval.py_value // right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.EQUAL_EQUAL:
                if left_eval.type in {TypeEnum.FLOAT, TypeEnum.INT, TypeEnum.BOOL}:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value == right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.LESS:
                if left_eval.type in {TypeEnum.FLOAT, TypeEnum.INT, TypeEnum.BOOL}:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value < right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.LESS_EQUAL:
                if left_eval.type in {TypeEnum.FLOAT, TypeEnum.INT, TypeEnum.BOOL}:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value <= right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.GREATER:
                if left_eval.type in {TypeEnum.FLOAT, TypeEnum.INT, TypeEnum.BOOL}:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value > right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.GREATER_EQUAL:
                if left_eval.type in {TypeEnum.FLOAT, TypeEnum.INT, TypeEnum.BOOL}:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value >= right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.AND:
                if left_eval.type == TypeEnum.BOOL:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value and right_eval.py_value
                    )

            elif operator_enum == OperatorEnum.OR:
                if left_eval.type == TypeEnum.BOOL:
                    return environment, Value(
                        TypeEnum.BOOL, left_eval.py_value or right_eval.py_value
                    )

        case Grouping(expression):
            return evaluate(environment, expression)

        case Unary(operator_enum, right):
            environment, right_eval = evaluate(environment, right)
            assert right_eval is not None

            if operator_enum == OperatorEnum.MINUS:
                if right_eval.type == TypeEnum.FLOAT:
                    return environment, Value(TypeEnum.FLOAT, -right_eval.py_value)

                elif right_eval.type == TypeEnum.INT:
                    return environment, Value(TypeEnum.INT, -right_eval.py_value)

            elif operator_enum == OperatorEnum.NOT:
                if right_eval.type == TypeEnum.BOOL:
                    return environment, Value(TypeEnum.BOOL, not right_eval.py_value)

        case _:
            raise Exception("Exhaustive switch error.")
