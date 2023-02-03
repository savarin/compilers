from typing import List, Tuple
import dataclasses

from scanner import TokenType, Token
from expression import (
    TypeEnum,
    OperatorEnum,
    Expr,
    Boolean,
    Integer,
    Float,
    Name,
    Type,
    Binary,
    Unary,
    Logical,
    Grouping,
    Assign,
    Call,
)
from statement import (
    DeclarationEnum,
    Statem,
    Break,
    Continue,
    Print,
    Declaration,
    If,
    Block,
    While,
    Expression,
    Function,
    Return,
)


class ParseError(Exception):
    ...


@dataclasses.dataclass
class Parser:
    tokens: List[Token]
    current: int


def init_parser(tokens: List[Token]) -> Parser:
    return Parser(tokens, 0)


def parse(parser: Parser) -> List[Statem]:
    statements: List[Statem] = []

    while not is_at_end(parser):
        parser, individual_statement = declaration(parser)
        statements.append(individual_statement)

    return statements


def declaration(parser: Parser) -> Tuple[Parser, Statem]:
    parser, is_function = match(parser, [TokenType.FUNCTION])

    if is_function:
        return function(parser)

    parser, is_variable = match(parser, [TokenType.CONST, TokenType.VAR])

    if is_variable:
        return variable_declaration(parser)

    return statement(parser)


def function(parser: Parser) -> Tuple[Parser, Statem]:
    parser, name = consume(parser, TokenType.IDENTIFIER, "Expect function name.")

    parser, _ = consume(parser, TokenType.LEFT_PAREN, "Expect '(' after function name.")

    parameter_names: List[Name] = []
    parameter_types: List[Type] = []

    if not expect(parser, TokenType.RIGHT_PAREN):
        while True:
            parser, parameter_name = consume(
                parser, TokenType.IDENTIFIER, "Expect parameter name."
            )
            parameter_names.append(Name(parameter_name.lexeme))

            parser, parameter_type = advance(parser)

            if parameter_type.token_type not in [
                TokenType.BOOL,
                TokenType.INT,
                TokenType.FLOAT,
            ]:
                raise ParseError("Expect parameter type.")

            parameter_types.append(Type(TypeEnum(parameter_type.token_type.value)))

            parser, is_comma = match(parser, [TokenType.COMMA])

            if not is_comma:
                break

    parser, _ = consume(parser, TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

    parser, return_type = advance(parser)

    if return_type.token_type not in [TokenType.BOOL, TokenType.INT, TokenType.FLOAT]:
        raise ParseError("Expect return type.")

    parser, _ = consume(parser, TokenType.LEFT_BRACE, "Expect '{' before body.")

    parser, body = block(parser)

    return parser, Function(
        Name(name.lexeme),
        parameter_names,
        parameter_types,
        Type(TypeEnum(return_type.token_type.value)),
        Block(body),
    )


def variable_declaration(parser: Parser) -> Tuple[Parser, Statem]:
    declaration_enum = DeclarationEnum(previous(parser).token_type.value)

    parser, name = consume(parser, TokenType.IDENTIFIER, "Expect variable name.")

    value_type = None
    parser, is_value_type = match(
        parser, [TokenType.BOOL, TokenType.INT, TokenType.FLOAT]
    )

    if is_value_type:
        value_type = Type(TypeEnum(previous(parser).token_type.value))

    initializer = None
    parser, is_equal = match(parser, [TokenType.EQUAL])

    if is_equal:
        parser, initializer = expression(parser)

    if declaration_enum == DeclarationEnum.CONST and not is_equal:
        raise ParseError("Require const to have a value.")

    parser, _ = consume(
        parser, TokenType.SEMICOLON, "Expect ';' after variable declaration."
    )

    return parser, Declaration(
        Name(name.lexeme), declaration_enum, value_type, initializer
    )


def statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, is_break = match(parser, [TokenType.BREAK])

    if is_break:
        return break_statement(parser)

    parser, is_continue = match(parser, [TokenType.CONTINUE])

    if is_continue:
        return continue_statement(parser)

    parser, is_if = match(parser, [TokenType.IF])

    if is_if:
        return if_statement(parser)

    parser, is_while = match(parser, [TokenType.WHILE])

    if is_while:
        return while_statement(parser)

    parser, is_print = match(parser, [TokenType.PRINT])

    if is_print:
        return print_statement(parser)

    parser, is_return = match(parser, [TokenType.RETURN])

    if is_return:
        return return_statement(parser)

    parser, is_block = match(parser, [TokenType.LEFT_BRACE])

    if is_block:
        parser, statements = block(parser)
        return parser, Block(statements)

    return expression_statement(parser)


def break_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, _ = consume(
        parser, TokenType.SEMICOLON, "Expect ';' after break statement."
    )

    return parser, Break()


def continue_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, _ = consume(
        parser, TokenType.SEMICOLON, "Expect ';' after continue statement."
    )

    return parser, Continue()


def if_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, condition = expression(parser)

    parser, then_branch = statement(parser)

    else_branch = None
    parser, is_then = match(parser, [TokenType.ELSE])

    if is_then:
        parser, else_branch = statement(parser)

    return parser, If(condition, then_branch, else_branch)


def while_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, condition = expression(parser)

    parser, body = statement(parser)

    return parser, While(condition, body)


def print_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, individual_expression = expression(parser)

    parser, _ = consume(
        parser, TokenType.SEMICOLON, "Expect ';' after print statement."
    )

    return parser, Print(individual_expression)


def return_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, value = expression(parser)

    parser, _ = consume(parser, TokenType.SEMICOLON, "Expect ';' after return value.")

    return parser, Return(value)


def block(parser: Parser) -> Tuple[Parser, List[Statem]]:
    statements: List[Statem] = []

    while not expect(parser, TokenType.RIGHT_BRACE) and not is_at_end(parser):
        parser, individual_statement = declaration(parser)

        if individual_statement is not None:
            statements.append(individual_statement)

    parser, _ = consume(parser, TokenType.RIGHT_BRACE, "Expect '}' after block.")

    return parser, statements


def expression_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, individual_expression = expression(parser)

    parser, _ = consume(parser, TokenType.SEMICOLON, "Expect ';' after expression.")

    return parser, Expression(individual_expression)


def expression(parser: Parser) -> Tuple[Parser, Expr]:
    return assignment(parser)


def assignment(parser: Parser) -> Tuple[Parser, Expr]:
    parser, or_expression = logic_or(parser)
    parser, is_equal = match(parser, [TokenType.EQUAL])

    if is_equal:
        equals = previous(parser)
        parser, value = assignment(parser)

        if isinstance(or_expression, Name):
            return parser, Assign(or_expression, value)

        raise error(parser, equals, "Invalid assignment target.")

    return parser, or_expression


def logic_or(parser: Parser) -> Tuple[Parser, Expr]:
    parser, and_expression = logic_and(parser)

    while True:
        parser, is_or = match(parser, [TokenType.OR])

        if not is_or:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = logic_and(parser)
        and_expression = Logical(and_expression, operator, right)

    return parser, and_expression


def logic_and(parser: Parser) -> Tuple[Parser, Expr]:
    parser, equality_expression = equality(parser)

    while True:
        parser, is_and = match(parser, [TokenType.AND])

        if not is_and:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = equality(parser)
        equality_expression = Logical(equality_expression, operator, right)

    return parser, equality_expression


def equality(parser: Parser) -> Tuple[Parser, Expr]:
    parser, comparison_expression = comparison(parser)

    while True:
        parser, is_equality = match(
            parser, [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        )

        if not is_equality:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = comparison(parser)
        comparison_expression = Binary(comparison_expression, operator, right)

    return parser, comparison_expression


def comparison(parser: Parser) -> Tuple[Parser, Expr]:
    parser, term_expression = term(parser)

    while True:
        parser, is_comparison = match(
            parser,
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ],
        )

        if not is_comparison:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = term(parser)
        term_expression = Binary(term_expression, operator, right)

    return parser, term_expression


def term(parser: Parser) -> Tuple[Parser, Expr]:
    parser, factor_expression = factor(parser)

    while True:
        parser, is_term = match(parser, [TokenType.PLUS, TokenType.MINUS])

        if not is_term:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = factor(parser)
        factor_expression = Binary(factor_expression, operator, right)

    return parser, factor_expression


def factor(parser: Parser) -> Tuple[Parser, Expr]:
    parser, unary_expression = unary(parser)

    while True:
        parser, is_factor = match(parser, [TokenType.STAR, TokenType.SLASH])

        if not is_factor:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = unary(parser)
        unary_expression = Binary(unary_expression, operator, right)

    return parser, unary_expression


def unary(parser: Parser) -> Tuple[Parser, Expr]:
    while True:
        parser, is_unary = match(parser, [TokenType.PLUS, TokenType.MINUS])

        if not is_unary:
            break

        operator = OperatorEnum(previous(parser).lexeme)
        parser, right = unary(parser)
        return parser, Unary(operator, right)

    return call(parser)


def call(parser: Parser) -> Tuple[Parser, Expr]:
    parser, primary_expression = primary(parser)

    while True:
        parser, is_parenthesis = match(parser, [TokenType.LEFT_PAREN])

        if not is_parenthesis:
            break

        parser, primary_expression = finish(parser, primary_expression)

    return parser, primary_expression


def finish(parser: Parser, callee: Expr) -> Tuple[Parser, Expr]:
    arguments: List[Expr] = []

    if not expect(parser, TokenType.RIGHT_PAREN):
        while True:
            parser, individual_expression = expression(parser)
            arguments.append(individual_expression)

            parser, is_comma = match(parser, [TokenType.COMMA])

            if not is_comma:
                break

    parser, _ = consume(parser, TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

    return parser, Call(callee, arguments)


def primary(parser: Parser) -> Tuple[Parser, Expr]:
    parser, is_number = match(parser, [TokenType.NUMBER])

    if is_number:
        value = previous(parser).lexeme
        return parser, Float(value) if "." in value else Integer(value)

    parser, is_boolean = match(parser, [TokenType.TRUE, TokenType.FALSE])

    if is_boolean:
        return parser, Boolean(previous(parser).lexeme)

    parser, is_identifier = match(parser, [TokenType.IDENTIFIER])

    if is_identifier:
        return parser, Name(previous(parser).lexeme)

    parser, is_parenthesis = match(parser, [TokenType.LEFT_PAREN])

    if is_parenthesis:
        parser, parenthesis_expression = expression(parser)
        parser, _ = consume(
            parser, TokenType.RIGHT_PAREN, "Expect ')' after expression."
        )

        return parser, Grouping(parenthesis_expression)

    raise error(parser, peek(parser), "Expect expression.")


def match(parser: Parser, token_types: List[TokenType]) -> Tuple[Parser, bool]:
    for token_type in token_types:
        if expect(parser, token_type):
            parser, _ = advance(parser)
            return parser, True

    return parser, False


def consume(
    parser: Parser, token_type: TokenType, message: str
) -> Tuple[Parser, Token]:
    if expect(parser, token_type):
        return advance(parser)

    raise ParseError(message)


def advance(parser: Parser) -> Tuple[Parser, Token]:
    if not is_at_end(parser):
        parser.current += 1

    return parser, previous(parser)


def expect(parser: Parser, token_type: TokenType) -> bool:
    if is_at_end(parser):
        return False

    return peek(parser).token_type == token_type


def peek(parser: Parser) -> Token:
    return parser.tokens[parser.current]


def previous(parser: Parser) -> Token:
    return parser.tokens[parser.current - 1]


def error(parser: Parser, token: Token, message: str) -> ParseError:
    print(f"Error at TokenType.{token.token_type.name} in line {token.line}: {message}")
    return ParseError()


def is_at_end(parser: Parser) -> bool:
    return peek(parser).token_type == TokenType.EOF
