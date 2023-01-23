from typing import List, Tuple
import dataclasses

from scanner import TokenType, Token
from expression import TypeEnum, Expr, Boolean, Integer, Name, Type
from statement import (
    DeclarationEnum,
    Statem,
    Break,
    Continue,
    Print,
    Declaration,
    If,
    Block,
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
    parser, is_variable = match(parser, [TokenType.CONST, TokenType.VAR])

    if is_variable:
        return variable_declaration(parser)

    return statement(parser)


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

    parser, is_print = match(parser, [TokenType.PRINT])

    if is_print:
        return print_statement(parser)

    parser, is_block = match(parser, [TokenType.LEFT_BRACE])

    if is_block:
        parser, statements = block(parser)
        return parser, Block(statements)

    raise ParseError()


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
    parser, _ = consume(parser, TokenType.TRUE, "Expect 'true' after 'if'.")

    parser, then_branch = statement(parser)

    else_branch = None
    parser, is_then = match(parser, [TokenType.ELSE])

    if is_then:
        parser, else_branch = statement(parser)

    return parser, If(Boolean("true"), then_branch, else_branch)


def print_statement(parser: Parser) -> Tuple[Parser, Statem]:
    parser, individual_expression = expression(parser)
    parser, _ = consume(
        parser, TokenType.SEMICOLON, "Expect ';' after continue statement."
    )

    return parser, Print(individual_expression)


def block(parser: Parser) -> Tuple[Parser, List[Statem]]:
    statements: List[Statem] = []

    while not expect(parser, TokenType.RIGHT_BRACE) and not is_at_end(parser):
        parser, individual_statement = declaration(parser)

        if individual_statement is not None:
            statements.append(individual_statement)

    parser, _ = consume(parser, TokenType.RIGHT_BRACE, "Expect '}' after block.")

    return parser, statements


def expression(parser: Parser) -> Tuple[Parser, Expr]:
    parser, token = advance(parser)

    return parser, Integer(token.lexeme)


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

    raise ParseError()


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


def is_at_end(parser: Parser) -> bool:
    return peek(parser).token_type == TokenType.EOF
