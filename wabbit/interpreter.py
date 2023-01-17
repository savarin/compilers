from typing import Dict, List, Optional, Tuple, Union
import dataclasses
import enum

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
from statement import (
    Block,
    Break,
    Continue,
    Declaration,
    Expression,
    If,
    Print,
    Statem,
    While,
)


class ControlFlowEnum(enum.Enum):
    NONE = "NONE"
    LOOP = "LOOP"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"


@dataclasses.dataclass
class Value:
    type: TypeEnum
    py_value: Union[bool, float, int]


@dataclasses.dataclass
class Environment:
    environment: Optional["Environment"]
    values: Dict[str, Optional[Value]]


def init_environment(environment: Optional["Environment"] = None) -> Environment:
    values: Dict[str, Optional[Value]] = {}

    if environment is not None:
        individual_environment = environment.environment
        individual_values = environment.values

        environment = Environment(
            environment=individual_environment, values=individual_values
        )

    return Environment(environment=environment, values=values)


def define(environment: Environment, name: str, value: Optional[Value]) -> Environment:
    environment.values[name] = value
    return environment


def get(environment: Environment, name: str) -> Optional[Value]:
    if name in environment.values:
        return environment.values[name]

    if environment.environment is not None:
        return get(environment.environment, name)

    raise Exception("Name not found across all environments.")


def assign(environment: Environment, name: str, value: Optional[Value]) -> Environment:
    if name in environment.values:
        environment.values[name] = value
        return environment

    if environment.environment is not None:
        environment.environment = assign(environment.environment, name, value)
        return environment

    raise Exception("Name not found across all environments.")


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
        interpreter, individual_result, _ = execute(interpreter, statement, False)
        result += individual_result

    return result


def execute(  # type: ignore[return]
    interpreter: Interpreter, statement: Statem, is_loop: bool
) -> Tuple[Interpreter, List[str], ControlFlowEnum]:
    match statement:
        case Block(statements):
            return execute_block(interpreter, statements, is_loop)

        case Break():
            return interpreter, [], ControlFlowEnum.BREAK

        case Continue():
            return interpreter, [], ControlFlowEnum.CONTINUE

        # TODO: Implement storing of const vs var type.
        case Declaration(name, _, _, initializer):
            declaration_result = None

            if initializer is not None:
                environment, declaration_result = evaluate(
                    interpreter.environment, initializer
                )

            interpreter.environment = define(
                interpreter.environment, name.text, declaration_result
            )
            return interpreter, [], ControlFlowEnum.NONE

        case Expression(expression):
            interpreter.environment, expression_result = evaluate(
                interpreter.environment, expression
            )

            if isinstance(expression_result, list):
                return interpreter, expression_result, ControlFlowEnum.NONE

            return (
                interpreter,
                [str(expression_result.py_value)]
                if expression_result is not None
                else [],
                ControlFlowEnum.NONE,
            )

        case If(condition, then_branch, else_branch):
            interpreter.environment, if_predicate = evaluate(
                interpreter.environment, condition
            )

            if if_predicate is not None and if_predicate.py_value:
                return execute(interpreter, then_branch, is_loop)

            elif else_branch is not None:
                return execute(interpreter, else_branch, is_loop)

            return interpreter, [], ControlFlowEnum.NONE

        case Print(expression):
            interpreter.environment, print_result = evaluate(
                interpreter.environment, expression
            )

            if isinstance(print_result, list):
                return interpreter, print_result, ControlFlowEnum.NONE

            return (
                interpreter,
                [str(print_result.py_value) if print_result is not None else "nil"],
                ControlFlowEnum.NONE,
            )

        case While(condition, body):
            while_result: List[str] = []

            while True:
                interpreter.environment, while_predicate = evaluate(
                    interpreter.environment, condition
                )

                if while_predicate is None or not while_predicate.py_value:
                    break

                interpreter, individual_result, control_flow_enum = execute(
                    interpreter, body, True
                )

                if control_flow_enum == ControlFlowEnum.BREAK:
                    break

                while_result += individual_result

            return interpreter, while_result, ControlFlowEnum.NONE

        case _:
            raise Exception(
                f"Exhaustive switch error on {statement.__class__.__name__}."
            )


def execute_block(
    interpreter: Interpreter,
    statements: List[Statem],
    is_loop: bool,
) -> Tuple[Interpreter, List[str], ControlFlowEnum]:
    result: List[str] = []
    previous = interpreter.environment

    try:
        interpreter.environment = init_environment(interpreter.environment)

        for statement in statements:
            interpreter, individual_result, control_flow_enum = execute(
                interpreter, statement, is_loop
            )

            result += individual_result

            if control_flow_enum in {ControlFlowEnum.BREAK, ControlFlowEnum.CONTINUE}:
                if is_loop:
                    break

                raise Exception(f"Not in loop for {control_flow_enum.value}.")

    finally:
        interpreter.environment = previous

    return interpreter, result, control_flow_enum


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
            raise Exception(
                f"Exhaustive switch error on {expression.__class__.__name__}."
            )
